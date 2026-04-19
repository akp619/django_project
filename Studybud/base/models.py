from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)     #one topic can have multiple rooms but room will have only one topic.

    def __str__(self):
        return self.name[:50]

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='participants', blank = True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # shows the data set ordering
    class Meta:
        # it shows recently created or updated items on top
        ordering = ('-updated', '-created')

        # it shows recently created or updated items on bottom
        # ordering = ('updated', 'created')

    # to give a name to a db dataset
    def __str__(self):
        return self.name

class Message(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # it shows recently created or updated items on top
        ordering = ('-updated', '-created')

    def __str__(self):
        return self.body[:30]
