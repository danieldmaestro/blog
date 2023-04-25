from django.urls import path
from . import views

app_name = "blog_app"

urlpatterns = [
    path('posts/', views.PostList.as_view(), name="post_list"),
    path("posts/<int:pk>", views.PostDetail.as_view(), name="post_detail"),
    path("category/", views.CategoryList.as_view(), name="category_list"),
    path("category/<int:pk>/", views.CategoryDetail.as_view(), name="category_detail"),
    path("category/<int:pk>/posts", views.CategoryPosts.as_view(), name="category_post"),
    path('posts/<int:post_id>/comments/', views.PostCommentList.as_view(), name='comment-list'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('posts/<int:post_id>/comments/<int:comment_id>/replies', views.CommentReplies.as_view(), name='comment-replies'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('weather/', views.WeatherAPIView.as_view(), name='weather')
    
]