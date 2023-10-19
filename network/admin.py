from django.contrib import admin
from .models import User, Post, Like, Follower, User_bio

# Register your models here.
admin.site.register(User)
admin.site.register(User_bio)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)