from django.db import models
from django.contrib.auth.models import User
import re
from django.core.exceptions import FieldDoesNotExist, FieldError, ValidationError


class Category(models.Model):

    # validators to check no special characters in the string
    def check_special_characters(self):
        custom_chars = "@_!#$%^&*()<>?/\\|}{~:]"
        pattern = re.compile(f"[{re.escape(custom_chars)}]")
        if pattern.search(self):
            raise ValidationError("Invalid special character")


    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True, validators=[check_special_characters])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"   # to keep the correct name in admin dashboard

    def __str__(self):
        return self.name

    def __repr__(self):
        print(self.name, "====repr===")
        return self.name

status_choices = ((0, "Draft"), (1, "Published"))

class Blog(models.Model):

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(null=True, blank=True, upload_to="uploads/%Y%m%d/")
    short_description = models.CharField(max_length=200)
    blog_body = models.TextField(max_length=2000)
    status = models.IntegerField(choices = status_choices, default=status_choices[0])
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    # save() is when a new record is created
    """
    Upon calling we are updating the value of slug.
    """
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class About(models.Model):

    name = models.CharField(max_length=100)
    body = models.TextField(max_length=2000)

    def __str__(self):
        return self.name


class SocialLinks(models.Model):

    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "social_links"   # to keep the correct name in admin dashboard


