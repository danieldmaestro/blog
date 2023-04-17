from django.contrib import admin
from .models import Post, Category, Comment, Contact

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Contact)
