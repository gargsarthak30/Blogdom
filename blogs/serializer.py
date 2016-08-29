from rest_framework import serializers
from .models import Post
from .models import UserBlogdom


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('blogger', 'heading', 'blog_content', 'upvotes', 'time')


class UserBlogdomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBlogdom
        fields = ('user', 'first_name', 'last_name', 'email', 'age', 'bio', 'description')

