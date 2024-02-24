from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
# Create your models here.

class User(AbstractUser):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    password = models.TextField(max_length=50)
    name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=250)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)