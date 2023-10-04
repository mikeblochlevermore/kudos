from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post, Like, Follower
from datetime import datetime
import json


def index(request):

    posts = Post.objects.all()

    return render(request, "network/index.html", {
        "posts": posts,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]

        new_post = Post(
            content=content,
            user=request.user,
            time=datetime.now(),
        )

        new_post.save()
        return HttpResponseRedirect(reverse("index"))


def like(request, post_id):
    if request.method == "POST":

        post = Post.objects.get(id=post_id)

        like = Like(
        post=post,
        user=request.user,
        time=datetime.now()
        )

        like.save()

        post.like_count = post.like_count + 1
        post.save()

        return HttpResponseRedirect(reverse("index"))


@csrf_exempt
@login_required
def view_posts(request):

    # Query for requested posts
    try:
        posts = Post.objects.all()
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return posts contents
    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)