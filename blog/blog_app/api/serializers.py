from rest_framework import serializers

from django.contrib.auth.models import User

from blog_app.models import Post, Comment, Category


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = "__all__"
        


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.id')
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'text', 'create_date', 'parent']


class CategorySerializer(serializers.ModelSerializer):
    # posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'posts']