from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .models import User, Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.http import JsonResponse
def index(request):
    form = PostForm()
    posts = Post.objects.all()

    paginator = Paginator(posts, 10)  # 10 posts per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj,
        "form": form
    })

def newpost(request):
    if request.method == "POST" and request.user.is_authenticated:
        form = PostForm(request.POST)


        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

        
            post.save()
            return HttpResponseRedirect(reverse("index"))

        else:

            return render(request, "network/index.html", {
                "form": form,
                "posts": Post.objects.all()
            })

    return render(request, "network/index.html", {
        "form": PostForm(),
        "posts": Post.objects.all()
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

# ``````````````````````````````````


# forms


# ``````````````````````````````````

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


# ``````````````````````````````````

# profile


# ``````````````````````````````````

def profile(request, username):
    target_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=target_user)
 

    paginator = Paginator(posts, 10)  # 10 posts per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        current_user = request.user

        is_owner = current_user.id == target_user.id

        following = current_user.following.filter(id=target_user.id).exists()

        return render(request, "network/profile.html",{
            "name":target_user,
            "posts":page_obj,
            "following": following,
            "is_owner":is_owner
                
            })
    else:
        return render(request, "network/profile.html",{
            "name":target_user,
            "posts":page_obj,
                    
            })



@login_required
@require_POST
def toggle_follow(request, username):
    # Get the profile of the person to follow/unfollow
    target_profile = get_object_or_404(User, username=username)
    user_profile = request.user

    # Prevent users from following themselves
    if user_profile == target_profile:
        return redirect('profile', username=username)

    # Toggle the relationship status
    if user_profile.following.filter(id=target_profile.id).exists():
        user_profile.following.remove(target_profile)
    else:
        user_profile.following.add(target_profile)

    return redirect('profile', username=username)


@login_required
@require_POST
def toggle_likes(request, postid):
    post = get_object_or_404(Post, id=postid)
    if request.user.liked_posts.filter(id=postid).exists():
        request.user.liked_posts.remove(post)

    else:
        request.user.liked_posts.add(post)


    return redirect("index")

@login_required
def edit(request, postid):
    post = get_object_or_404(Post, id=postid)
    if request.user != post.author:
        return redirect("index")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = PostForm(instance=post)
    return render(request, "network/edit.html",{
        "form":form,
        "post": post
    })



@login_required
def following(request):
    posts = Post.objects.filter(
        author__in=request.user.following.all()
    )


    paginator = Paginator(posts, 10)  # 10 posts per page

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": page_obj
    })
    