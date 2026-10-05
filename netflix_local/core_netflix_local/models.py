from django.db import models
from django.contrib.auth.models import User
import uuid
import mimetypes
from django.core.files.storage import default_storage
from tinytag import TinyTag
from django.core.exceptions import ValidationError

# Create your models here.
class UserOTPValidator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{[self.otp]} {self.user.username}"

AGE_CHOICES = [
    ('Kids', 'Kids'),
    ('Adult', 'Adult'),
]
MOVIE_CHOICES = [
    ('Movie', 'movie'),
    ('Series', 'series'),
]

class ViewerProfile(models.Model):
    name = models.CharField(max_length=120)
    age = models.CharField(max_length=50, choices=AGE_CHOICES)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name='viewer_profile')

    class Meta:
        verbose_name = "ViewerProfile"   # to keep the correct name in admin dashboard
        verbose_name_plural = "ViewerProfiles"

    def __str__(self):
        return self.name

def movie_content_file_name(instance, filename):
    return "/".join(["Movies", instance.title, str(instance.uuid), filename])

class Movie(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=500)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    movie_type = models.CharField(choices=MOVIE_CHOICES)
    genre = models.ManyToManyField('Genre', blank=True)
    released = models.DateField(blank=True, null=True)
    runtime = models.CharField(max_length=20, null=True, blank=True)
    awards = models.CharField(max_length=100, null=True, blank=True)
    rating = models.FloatField(default=0.00, null=True, blank=True)
    rated = models.ForeignKey('Rated', on_delete=models.SET_NULL, blank=True, null=True)
    countries = models.ManyToManyField('Country', blank=True, related_name='countries')
    languages = models.ManyToManyField('Language', blank=True, related_name='languages')
    imdb_id = models.CharField(unique=True, null=True, blank=True)
    directors = models.ManyToManyField('FilmPersons', blank=True, related_name='directors')
    writer = models.ManyToManyField('FilmPersons', blank=True, related_name='writer')
    actors = models.ManyToManyField('FilmPersons', blank=True, related_name='actors')
    poster = models.URLField(max_length=1000, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    only_on_netflix = models.BooleanField(null=True, default=None, blank=True)
    video_file = models.FileField(upload_to=movie_content_file_name, blank=True, null=True)

    class Meta:
        verbose_name = "Movie"   # to keep the correct name in admin dashboard
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title

    def clean(self):
        """
        Custom object-level validation logic.
        """
        super().clean()
        if str(self.video_file):
            mime_type, _ = mimetypes.guess_type(str(self.video_file))
            if mime_type != "video/mp4":
                raise ValidationError("Provide a acceptable video format like mp4.")
            if self.movie_type!="Movie":
                raise ValidationError("Please Upload Episodes in the Episodes Lists.")

    def save(self, *args, **kwargs):
        self.full_clean()
        res = super().save()
        movie_metadata = VideoFile.objects.filter(movie=self)
        if not movie_metadata:
            if self.video_file:
                file_data = str(self.video_file).split("/")
                file_size = self.video_file.size
                object_name = file_data[-1]
                bucket_name = file_data[:len(file_data) - 2]
                mime_type, _ = mimetypes.guess_type(str(self.video_file))

                # get video file duration
                with default_storage.open(str(self.video_file), 'rb') as storage_file:
                    tag = TinyTag.get(file_obj=storage_file)

                # create video metadata
                VideoFile.objects.create(
                    movie=self,
                    bucket_name="/".join(bucket_name),
                    object_name=object_name,
                    file_size=file_size,
                    content_type=mime_type,
                    duration=tag.duration / 60 if tag.duration else 0
                )
        elif movie_metadata[0].bucket_name != str(self.video_file):
            movie_metadata[0].bucket_name = str(self.video_file)
        return res

class Genre(models.Model):
    name = models.CharField(max_length=120, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.name

class Season(models.Model):
    name = models.CharField(max_length=120)
    season = models.CharField(max_length=3, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'movie'],
                name='unique_season_name_and_movie'
            )
        ]

    def __str__(self):
        return f"[{self.movie.title}] {self.name}"

def series_content_file_name(instance, filename):
    return "/".join(["Episodes", instance.season.movie.title + " " + "S"+instance.season.season + " " +"e"+instance.episode, str(instance.uuid), filename])

class Episode(models.Model):
    title = models.CharField(max_length=120)
    released = models.DateField(blank=True, null=True)
    episode = models.CharField(max_length=3, blank=True, null=True)
    runtime = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(max_length=500)
    episode_id = models.CharField(max_length=120, unique=True, blank=True, null=True)
    season = models.ForeignKey('Season', on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    poster = models.URLField(max_length=1000, blank=True, null=True)
    video_file = models.FileField(upload_to=series_content_file_name, blank=True, null=True)

    def __str__(self):
        return f"[{self.season.movie.title}]  S-{self.season.season} Ep-{self.episode} {self.title}"

    def clean(self):
        """
        Custom object-level validation logic.
        """
        print("clean called episode")
        super().clean()
        if str(self.video_file):
            mime_type, _ = mimetypes.guess_type(str(self.video_file))
            if mime_type != "video/mp4":
                raise ValidationError("Provide a acceptable video format like mp4.")

    def save(self, *args, **kwargs):
        self.full_clean()
        res = super().save()
        episode_metadata = VideoFile.objects.filter(episode=self)
        if not episode_metadata:
            if self.video_file:
                file_data = str(self.video_file).split("/")
                file_size = self.video_file.size
                object_name = file_data[-1]
                bucket_name = file_data[:len(file_data) - 2]
                mime_type, _ = mimetypes.guess_type(str(self.video_file))

                # get video file duration
                with default_storage.open(str(self.video_file), 'rb') as storage_file:
                    tag = TinyTag.get(file_obj=storage_file)

                # create video metadata
                VideoFile.objects.create(
                    episode=self,
                    bucket_name="/".join(bucket_name),
                    object_name=object_name,
                    file_size=file_size,
                    content_type=mime_type,
                    duration=tag.duration / 60 if tag.duration else 0
                )
        elif episode_metadata[0].bucket_name != str(self.video_file):
            episode_metadata[0].bucket_name = str(self.video_file)
        return res

class Rated(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class FilmPersons(models.Model):
    name = models.CharField(max_length=120, unique=True)
    roles = models.ManyToManyField('MovieRole', blank=True, related_name='writer')

    def __str__(self):
        return self.name

class MovieRole(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name

class VideoFile(models.Model):
    movie = models.OneToOneField(
        Movie,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    episode = models.OneToOneField(
        Episode,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    bucket_name = models.CharField(max_length=100)
    object_name = models.CharField(max_length=500)

    file_size = models.BigIntegerField(null=True, blank=True)
    content_type = models.CharField(max_length=100, blank=True)

    duration = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

class WatchHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(ViewerProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.user.username}][{self.profile.name}]-{self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.movie:
            self.genre.add(*self.movie.genre.all())