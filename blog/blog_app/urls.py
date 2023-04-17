from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/reply/', views.add_reply, name='add_reply'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('search', views.search_view, name="search"),
]
