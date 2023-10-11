from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
   content = models.CharField(max_length=264)
   time = models.DateTimeField(auto_now_add=True)
   like_count = models.IntegerField(default=0)
   image_url = models.CharField(max_length=128)

   def serialize(self):
        return {
            "id": self.id,
            "user": f"{self.user}",
            "content": self.content,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "like_count": self.like_count,
            "image_url": self.image_url
        }


class Like(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like")
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")
   time = models.DateTimeField()

   def serialize(self):
        return {
            "id": self.id,
            "user": f"{self.user}",
            "post": f"{self.post}",
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
        }


class Follower(models.Model):
    # user = the person being followed
    # follower = the person following this user
    # therefore the follower is FOLLOWING the user
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
   follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

   def __str__(self):
        return f"{self.user}, {self.follower}"
