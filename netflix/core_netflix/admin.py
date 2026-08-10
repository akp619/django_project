from django.contrib import admin
from .models import UserOTPValidator, ExtendUserProfile, CustomerProfile, Movie, Video

# Register your models here.
admin.site.register(ExtendUserProfile)
admin.site.register(UserOTPValidator)
admin.site.register(CustomerProfile)
admin.site.register(Movie)
admin.site.register(Video)
