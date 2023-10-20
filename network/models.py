from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class User_bio(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bio")
   bio = models.CharField(max_length=264, default=None)
   bio_image_url = models.CharField(max_length=264, default=None)

   def __str__(self):
        return f"{self.user}, {self.bio}, , {self.bio_image_url}"


class Post(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
   content = models.CharField(max_length=264)
   time = models.DateTimeField(auto_now_add=True)
   like_count = models.IntegerField(default=0)
   image_url = models.CharField(max_length=128)

   def serialize(self, current_user):
        # Includes an image of the user for each post
        bio_image = User_bio.objects.get(user=self.user).bio_image_url

        # Checks to see if the current user has already liked that post and sets a true/false status
        like = Like.objects.filter(post=self.id, user=current_user)
        if like.exists():
            liked = True
        else:
            liked = False

        # If the current user owns the post, send a token that they can edit the post
        if self.user == current_user:
            can_edit = True
        else:
            can_edit = False

        return {
            "id": self.id,
            "user": f"{self.user}",
            "bio_image": bio_image,
            "content": self.content,
            "time": self.time.strftime("%b %d %Y, %I:%M %p"),
            "like_count": self.like_count,
            "image_url": self.image_url,
            "liked": liked,
            "can_edit": can_edit,
        }


class Like(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like")
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")
   time = models.DateTimeField(auto_now_add=True)

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
