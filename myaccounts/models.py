from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class MyUser(AbstractUser):
   email = models.EmailField(max_length=50, unique=True, primary_key=True)
   nickname = models.CharField(max_length=50)
   gender = models.CharField(max_length=20)
   birth = models.CharField(max_length=8)
   
   def __str__(self):
       return self.nickname