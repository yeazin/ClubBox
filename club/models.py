
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.fields import CharField, NullBooleanField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
import uuid


class CustomUserManager(BaseUserManager):
    """custom user email where email is unique.
    We can also pass Full name , email and password here"""

    def create_user(self, email,password, **extra_fields):
        """Create and save a User given email and password"""
        if not email:
            raise ValueError(_("The Email is must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save Super user with given email address"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Supperuser must have is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Supperuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(_('email_address'), unique=True)

    password = models.CharField(max_length=200)
    confirm_password = models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

# abstract class 
class TimeSince(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

# Gender Class
class Gender(models.Model):
    name = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name 
# Admin Class
class Admin (TimeSince):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='admin')
    image = models.ImageField(upload_to = 'user/admin', null=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')

    def __str__(self):
        return self.name 

# Member Class 
class Member(TimeSince):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='member')
    image = models.ImageField(upload_to = 'user/member', null=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    f_name = models.CharField(max_length=300, null=True, blank=True, verbose_name='Father`s Name')
    m_name = models.CharField(max_length=300, null=True, blank=True, verbose_name='Mother`s Name')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    dob = models.DateField(auto_now= False, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')
    nationality = models.CharField(max_length=100, null=True)
    present_address = models.CharField(max_length=400, null=True, verbose_name='Present Address')
    parmanent_address = models.CharField(max_length=400, null=True, verbose_name='Parmanent Address')
    nid = models.CharField(max_length=16, null=True)

    def __str__(self):
        return str(self.name) 


