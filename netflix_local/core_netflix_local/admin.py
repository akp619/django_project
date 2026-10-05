from django.contrib import admin
from .models import (UserOTPValidator, ViewerProfile, Movie, Genre,
                     Season, Episode, Rated, FilmPersons, MovieRole,
                     Country, Language, VideoFile, WatchHistory)

class WatchHistoryAdmin(admin.ModelAdmin):
    # Exclude it so Django Admin form ignores it and doesn't wipe it out
    exclude = ('genre',)

# Register your models here.
admin.site.register(UserOTPValidator)
admin.site.register(ViewerProfile)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Season)
admin.site.register(Episode)
admin.site.register(Rated)
admin.site.register(FilmPersons)
admin.site.register(MovieRole)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(VideoFile)
admin.site.register(WatchHistory, WatchHistoryAdmin)