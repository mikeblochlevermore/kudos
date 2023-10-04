
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("<int:post_id>/like", views.like, name="like"),

    # API Routes
    path("view_posts", views.view_posts, name="view_posts"),
    path("like/<int:post_id>", views.like, name="like"),
]
