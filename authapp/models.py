from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, verbose_name='email')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='age')
    avatar = models.ImageField(upload_to='users', null=True, blank=True, verbose_name='avatar')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['username']

