from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from boards_app.models import Board




class CustomUserManager(BaseUserManager):
    def create_user(self, email, fullname, password, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        if not fullname:
            raise ValueError("Full Name is required")

        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, fullname, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, fullname, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'fullname'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.fullname
