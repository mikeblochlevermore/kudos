
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("edit_bio", views.edit_bio, name="edit_bio"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.view_following, name="following"),

    # API Routes
    path("view_posts/<str:filter>/<int:page>", views.view_posts, name="view_posts"),
    path("like/<int:post_id>", views.like, name="like"),
    path("profile/<str:username>/follow", views.follow, name="follow"),
]
