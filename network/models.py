from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
   content = models.CharField(max_length=264)
   time = models.DateTimeField()
   like_count = models.IntegerField(default=0)

   def __str__(self):
        return f"{self.user}, {self.content}, {self.time}"


class Like(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like")
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")
   time = models.DateTimeField()

   def __str__(self):
        return f"{self.user}, {self.post}, {self.time}"


class Follower(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
   follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

   def __str__(self):
        return f"{self.user}, {self.follower}"
