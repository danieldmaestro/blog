from rest_framework import serializers

from django.contrib.auth.models import User

from blog_app.models import Post, Comment, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__ "
        


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'posts']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']