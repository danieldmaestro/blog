from django.urls import path
from . import views

app_name = "blog_app"

urlpatterns = [
    path('posts/', views.PostList.as_view(), name="post_list"),
    path("posts/<int:pk>", views.PostDetail.as_view(), name="post_detail"),
    path("category/", views.CategoryList.as_view(), name="category_list"),
    path("category/<int:pk>", views.CategoryDetail.as_view(), name="category_detail"),
    path('posts/<int:pk>/comments', views.CommentList.as_view(), name="comment_list"),
    path('posts/<int:pk>/comments/', views.CommentDetail.as_view(), name="comment_detail"),
]