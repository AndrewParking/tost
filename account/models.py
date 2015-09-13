from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class AccountManager(BaseUserManager):

    def create_user(self, username, email, password=None, **kwargs):
        account = self.model(
            username=username,
            email=email
        )

        account.set_password(password)

        if kwargs.get('tagline'):
            account.tagline = kwargs['tagline']
        if kwargs.get('description'):
            account.description = kwargs['description']

        account.save()
        return account

    def create_superuser(self, username, email, password=None, **kwargs):
        account = self.create_user(username, email, password, **kwargs)
        account.is_admin = True
        account.save()
        return Account


class Account(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    tagline = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = AccountManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not kwargs.get('username') and not self.username:
            raise ValidationError('We need your username')
        if not kwargs.get('email') and not self.email:
            raise ValidationError('We need your email')
        super(Account, self).save(*args, **kwargs)