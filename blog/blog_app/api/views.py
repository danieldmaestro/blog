from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


from blog_app.models import Post, Comment, Category
from .serializers import CommentSerializer, PostSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly



class PostList(generics.ListCreateAPIView):
    """Lists all Posts and exposes Create endpoint for authenticated users"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieves Post and all comments associated in a detail view. Update & Destroy only if authenticated"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        comments = instance.comments.all()  # Get all comments related to the post
        comments_serializer = CommentSerializer(comments, many=True, context={'request': request})
        data = {
            'post': serializer.data,
            'comments': comments_serializer.data
        }
        return Response(data)

    


class CommentList(generics.ListAPIView):
    """Lists all comments for Post"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(post_id = self.kwargs['post_id'])
        return queryset


class CommentDetail(generics.RetrieveDestroyAPIView):
    """Detail view for comment that uses both Post and Comment pk to retrieve. Destroy View for only authenticated users"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'], post=post)
        return comment


class CategoryList(generics.ListCreateAPIView):
    """Lists all Categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class CategoryDetail(generics.RetrieveAPIView):
    """Retrieves Category detail with pk including all related posts"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        """Retrieves all posts under a category and displays in the detail view"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        posts = instance.posts.all()[:10]  # Get all comments related to the post
        posts_serializer = PostSerializer(posts, many=True, context={'request': request})
        data = {
            'category': serializer.data,
            'posts': posts_serializer.data
        }
        return Response(data)
    
class CategoryPosts(generics.ListAPIView):
    """This Category endpoint returns first 10 posts in a given category"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(pk = self.kwargs['pk'])
        return queryset
    
class SearchView(generics.ListAPIView):
    """Takes query, return List View of queryset filtered using query based on title of posts"""
    def get(self, request, format=None):
        query = request.GET.get('q', '')
        if query:
            posts = Post.objects.filter(title__icontains=query)
        else:
            posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    # queryset = Post.objects.all()
    # serializer_class = PostSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ['title']
        
        




# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

