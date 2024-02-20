from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView
from .models import Post, Comment
from .forms import CommentForm, EditForm
from django.contrib import messages
from django.urls import reverse_lazy


class PostList(generic.ListView):
    """
    View for displaying all blog posts on blog page,
    including filter by approved and order by date descending,
    paginated by 6 blog posts on each page
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):
    """
    View for displaying individual blog posts on a single page,
    including features to add a comment or like
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Get method to retrieve post details including comments and likes
        and render post detail page
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        """
        Post method to validate comment input, save and re-load
        post detail page
        Success message as user feedback
        """
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLike(LoginRequiredMixin, View):
    """
    View to remove or add like on post detail page
    """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CommentUpdateView(UpdateView):
    """
    View to allow users to update their comment
    on the post detail page
    """
    model = Comment
    form_class = EditForm
    template_name = 'comment_form.html'

    success_url = reverse_lazy('home')


def delete_comment(request, slug, comment_id):
    """
    View to allow users to delete their comment
    on the post detail page
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.name == request.user.username:
        comment.delete()
        messages.add_message(
                request, messages.SUCCESS, 'Comment has been deleted.')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own comments.')

    return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def handler404(request, exception):
    """
    Custom 404 page
    """
    return render(request, "errors/404.html", status=404)


def handler500(request):
    """
    Custom 500 page
    """
    return render(request, "errors/500.html", status=500)


def handler403(request, exception):
    """
    Custom 403 page
    """
    return render(request, "errors/403.html", status=403)


def handler405(request, exception):
    """
    Custom 405 page
    """
    return render(request, "errors/405.html", status=405)
