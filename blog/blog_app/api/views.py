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

import requests
from rest_framework import status



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

    def get_queryset(self):
        return super().get_queryset().prefetch_related('comments')

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

    
class PostCommentList(generics.ListCreateAPIView):
    """Lists all comments for Post and create comment"""
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id = self.kwargs['post_id'])


class CommentDetail(generics.RetrieveDestroyAPIView):
    """Detail view for comment that uses both Post and Comment pk to retrieve. Destroy View for only authenticated users"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


    def get_object(self):
        # post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'], post_id=self.kwargs['post_id'])
        return comment
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieves all replies under a comment and displays in the detail view"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        replies = instance.replies.all()  # Get all replies related to the comment
        replies_serializer = CommentSerializer(replies, many=True, context={'request': request})
        data = {
            'comment': serializer.data,
            'replies': replies_serializer.data
        }
        return Response(data)


class CommentReplies(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent = self.kwargs['comment_id'])

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
            'last_ten_posts': posts_serializer.data
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
    

class WeatherAPIView(APIView):
    def get(self, request, *args, **kwargs):
        
        location = request.GET.get('location')
        date = request.GET.get('date')
        key = 'a5df6a8757bf4216b21134024232504'

        if not location:
            return Response({'error': 'Please provide a location.'}, status=status.HTTP_400_BAD_REQUEST)
        
        url = f'https://api.weatherapi.com/v1/forecast.json?key={key}&q={location}&dt={date}'
        response = requests.get(url)

        if response.status_code != 200:
            return Response({'error': 'Failed to retrieve weather information.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = response.json()
        
        if date:
            location = data['location']['name']
            date = data['forecast']['forecastday'][0]['date']
            country = data['location']['country']
            temperature_c = data['forecast']['forecastday'][0]['day']['avgtemp_c']
            temperature_f = data['forecast']['forecastday'][0]['day']['avgtemp_f']
            condition = data['forecast']['forecastday'][0]['day']['condition']['text']

            response_data = {
                'location' : location,
                'date' : date,
                'country' : country,
                'temperature in celsius': temperature_c,
                'temperature in fahrenheit': temperature_f,
                'condition': condition,
            }
            return Response({'forecast' : response_data}, status=status.HTTP_200_OK)

        else:
            response_data = {
                'location': data['location']['name'],
                'country': data['location']['country'],
                'local time': data['location']['localtime'],
                'temperature in celsius': data['current']['temp_c'],
                'temperature in fahrenheit': data['current']['temp_f'],
                'condition': data['current']['condition']['text'],
                'wind speed in kph': data['current']['wind_kph'],
            }
            return Response({'current_report': response_data}, status=status.HTTP_200_OK)
        

            




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

