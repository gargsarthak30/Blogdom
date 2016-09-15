from django import forms
from .models import UserBlogdom, Post


class UserBlogdomForm(forms.ModelForm):

    class Meta:
        model = UserBlogdom
        fields = ('first_name', 'last_name', 'age', 'bio', 'description', 'profile_picture', 'cover_picture')
        widgets = {'description': forms.Textarea}

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('heading', 'blog_content', 'image')
        widgets = {"blog_content": forms.Textarea, "heading": forms.Textarea}


