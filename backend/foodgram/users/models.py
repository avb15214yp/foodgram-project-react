from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

ROLE_USER = 'user'
ROLE_ADMIN = 'admin'

ROLES = [
    (ROLE_USER, 'Пользователь'),
    (ROLE_ADMIN, 'Администратор')
]


class CustomUserManager(UserManager):

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not extra_fields.get('first_name'):
            raise ValueError('First name is required')
        if not extra_fields.get('last_name'):
            raise ValueError('Last name is required')
        if username == 'me':
            raise ValueError('"me" is invalid username')
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role=ROLE_ADMIN, **extra_fields):
        return super().create_superuser(
            username, email, password, role=role, **extra_fields)


class User(AbstractUser):

    email = models.EmailField("email адрес", unique=True, db_index=True)
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)

    role = models.CharField(
        choices=ROLES,
        default=ROLE_USER,
        max_length=200,
        verbose_name='Роль',
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ROLES[1][0]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower'
    )

    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self):
        return self.user.username + '->' + self.following.username
