
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/follow", views.toggle_follow, name="toggle_follow"),
    path("post/<int:postid>/", views.toggle_likes, name="toggle_likes"),
    path("posts/<int:postid>/edit", views.edit, name="edit"),
    path("following", views.following, name="following")
]
