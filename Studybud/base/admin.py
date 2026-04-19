from django.contrib import admin

# Register your models here.


# To view our custom tables in the admin panel we need to register our models in the admin panel

# First import model
from .models import Topic
from .models import Room
from .models import Message

# Register the model
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Message)