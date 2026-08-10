from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import uuid

# Create your models here.
class ExtendUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, blank=False)
    mobile = models.CharField(max_length=10, unique=True)
    customer_profile = models.ManyToManyField('CustomerProfile', blank=True)

    def __str__(self):
        return self.user.username if self.user else ''

class UserOTPValidator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{[self.otp]} {self.user.username}"

AGE_CHOICES = [
    ('Kids', 'Kids'),
    ('Adult', 'Adult'),
]
MOVIE_CHOICES = [
    ('Seasonal', 'Seasonal'),
    ('Single', 'Single'),
]

class CustomerProfile(models.Model):
    name = models.CharField(max_length=120)
    age = models.CharField(max_length=50, choices=AGE_CHOICES)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True)

    class Meta:
        verbose_name = "CustomerProfile"   # to keep the correct name in admin dashboard
        verbose_name_plural = "CustomerProfiles"

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True)
    movie_type = models.CharField(choices=MOVIE_CHOICES)
    videos = models.ManyToManyField('Video', blank=True)
    flyer = models.ImageField(blank=True, null=True, upload_to='flyer')
    age_limit = models.CharField(max_length=10, choices=AGE_CHOICES)

    class Meta:
        verbose_name = "Movie"   # to keep the correct name in admin dashboard
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=120)
    file = models.FileField(upload_to='movies')

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

