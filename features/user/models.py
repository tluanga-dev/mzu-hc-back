# models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_id, password=None, **extra_fields):
        """Creates and saves a new user with the given email, user_id, and password."""
        if not email:
            raise ValueError('The Email field must be set')
        if not user_id:
            raise ValueError('The User ID field must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id, password, **extra_fields):
        """Creates and saves a new superuser with the given email, user_id, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, user_id, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_id = models.CharField(max_length=255, unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email',]

    def save(self, *args, **kwargs):
        if self.pk is not None:  # the instance already exists in the database
            orig = CustomUser.objects.get(pk=self.pk)
            if orig.user_id != self.user_id:  # the user_id is being changed
                raise ValueError("user_id cannot be changed after it's set")
        super().save(*args, **kwargs)

    class Meta:
        app_label = "user"

    def __str__(self):
        return self.email
