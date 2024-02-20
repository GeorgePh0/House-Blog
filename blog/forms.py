from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    Form for comments
    """
    class Meta:
        model = Comment
        fields = ('body',)


class EditForm(forms.ModelForm):
    """
    Form for editing comments
    """
    class Meta:
        model = Comment
        fields = ('body',)
