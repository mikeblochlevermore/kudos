from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Like, Follower
from datetime import datetime
import json


def index(request):

    return render(request, "network/index.html", {
    })


def view_following(request):

    return render(request, "network/following.html", {
    })


def profile(request, username):

    user = User.objects.get(username=username)

    followers = Follower.objects.filter(user=user)
    follower_count = followers.count()

    following = Follower.objects.filter(follower=user)
    following_count = following.count()

    return render(request, "network/profile.html", {
        "username": username,
        "followers":  followers,
        "follower_count": follower_count,
        "following": following,
        "following_count": following_count,
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



@csrf_exempt
@login_required
def view_posts(request, filter, page):

    if request.method == "GET":

    # Options for the "filter" variable:
    # "all" to view all posts
    # "following" to see posts from people the user is following
    # "{username}" to see posts from just that specific user

        if filter == "all":
            # Query for all posts
            try:
                posts = Post.objects.all().order_by('-time')

            except Post.DoesNotExist:
                return JsonResponse({"error": "Posts not found."}, status=404)

        elif filter == "following":
            # Query for posts from people that user is following
            try:
                # looks up current user
                user = User.objects.get(username=request.user)
                # looks up accounts which have the current user as their follower (i.e. people the user is following)
                list = Follower.objects.filter(follower=user)

                # Creates a list of users that the current user follows
                following_list = []
                for pair in list:
                    following_list.append(pair.user)

                # Filters for just posts from accounts the current user follows
                posts = Post.objects.filter(user__in=following_list).order_by('-time')
            except Post.DoesNotExist:
                return JsonResponse({"error": "Posts not found."}, status=404)

        else:
            # Query for selected posts by that username
            try:
                user = User.objects.get(username=filter)
                posts = Post.objects.filter(user=user).order_by('-time')
            except Post.DoesNotExist or User.DoesNotExist:
                return JsonResponse({"error": "Posts not found."}, status=404)

        # Paginator divides the posts to 10 per page
        paginator = Paginator(posts, 1)
        data = paginator.get_page(page)

        # Returns posts data as defined above
        return JsonResponse([post.serialize() for post in data], safe=False)

        # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)



@csrf_exempt
@login_required
def like(request, post_id):

        if request.method == "GET":
            post = Post.objects.get(id=post_id)
            # Searches for a like already made by the current user on this post
            like = Like.objects.filter(post=post, user=request.user)

            if like.exists():
                return JsonResponse(True, safe=False)
            else:
                return JsonResponse(False, safe=False)

        if request.method == "PUT":
            post = Post.objects.get(id=post_id)
            like = Like.objects.filter(post=post, user=request.user)

            if like.exists():
                # If the post is liked by the user already, deletes the like from the database
                like.delete()

                # Updates the like_count in the Post model (adds -1 from data)
                data = json.loads(request.body)
                post.like_count = post.like_count + data["like_count"]
                post.save()

                # ADD A EXPECT TEST HERE TO CHECK THE DATA INCLUDES THE RIGHT INFO

            else:
                # Adds a new like in the Like model
                new_like = Like(
                    user=request.user,
                    post=post,
                    time=datetime.now(),
                )
                new_like.save()

                # Updates the like count in the Post model (adds 1 from data)
                data = json.loads(request.body)
                post.like_count = post.like_count + data["like_count"]
                post.save()

        return HttpResponse(status=204)


@csrf_exempt
@login_required
def follow(request, username):

    user = User.objects.get(username=username)
    # checks to see if the account is already followed by the current user

    if request.method == "GET":
            followed = Follower.objects.filter(user=user, follower=request.user)
            # returns information to frontend on whether the account is already followed by the current user
            if followed.exists():
                return JsonResponse(True, safe=False)
            else:
                return JsonResponse(False, safe=False)

    if request.method == "PUT":

        followed = Follower.objects.filter(user=user, follower=request.user)
        # If the account is already followed by the user, deletes the relationship from the database
        if followed.exists():
            followed.delete()
            print("unfollowed")

        else:
            new_follow = Follower(
            user=user,
            follower=request.user)
            print(f"New Follow: USER:", new_follow.user, "FOLLOWER", new_follow.follower)
            new_follow.save()

    return HttpResponse(status=204)