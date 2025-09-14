from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model

    class Meta:
        permissions = [
            ("can_view","can_create","can_edit","can_delete" )
        ]

    def __str__(self):
        return self.title
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    profile_photo = models.ImageField(_('profile photo'), upload_to='profile_photos/', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email