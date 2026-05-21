from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# post model

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User)