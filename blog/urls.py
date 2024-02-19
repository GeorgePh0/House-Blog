from . import views
from django.urls import path
from .views import CommentUpdateView

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path(
        'comment_form/<int:pk>',
        CommentUpdateView.as_view(),
        name='comment_form'),
    path(
            'delete_comment/<str:slug>/<int:comment_id>/',
            views.delete_comment,
            name='delete_comment'),
]
