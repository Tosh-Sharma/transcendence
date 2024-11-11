import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, default='example@example.com')  # Provide a default value
    password = models.CharField(max_length=128)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player1 = models.ForeignKey(
        'User', related_name='games_as_player1', on_delete=models.CASCADE
    )
    player2 = models.ForeignKey(
        'User', related_name='games_as_player2', on_delete=models.CASCADE
    )
    score1 = models.IntegerField()
    score2 = models.IntegerField()
    is_tournament = models.BooleanField(default=False)

    def __str__(self):
        return f"Game: {self.player1.username} vs {self.player2.username}"

class PlayerSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        'User', related_name='settings', on_delete=models.CASCADE
    )
    background_color = models.CharField(max_length=50)
    paddle_color = models.CharField(max_length=50)

    def __str__(self):
        return f"Settings for {self.player.username}"
