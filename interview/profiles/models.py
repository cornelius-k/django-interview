from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import EmailValidator

from django.contrib.auth.base_user import BaseUserManager


class UserProfileManager(BaseUserManager):
    '''
    Custom User Manager for User Profile that uses email in the place
    of username
    '''
    def create_user(self, email, password, **extra_fields):

        # validate email is valid
        EmailValidator()(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):

        # validate email is valid
        EmailValidator()(email)
        email = self.normalize_email(email)
        
        # set superuser fields
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

class UserProfile(AbstractUser):
    '''
    Custom User Model uses email as username field
    '''
    username = None
    email = models.EmailField(unique=True)
    objects = UserProfileManager()
    avatar = models.ImageField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
