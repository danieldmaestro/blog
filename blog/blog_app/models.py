from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    post_image = models.ImageField(upload_to='project_media/', null=True)
    category = models.ManyToManyField('Category', blank=True, related_name='posts')
    publish_date = models.DateTimeField(auto_now_add=True)
    num_views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
    
    @property
    def comments(self):
        return self.comments.all()


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=400)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'room_table'

    def __str__(self) -> str:
        return self.name
    
    