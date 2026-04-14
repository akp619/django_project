from django.contrib import admin
from .models import Category, Blog, About, SocialLinks


# to pre-populate slug [slug is like convert "test blog" to some readable url like "base_url/test-blog"]
class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['title', 'category', 'author', 'status', 'is_featured'] # display all these mentioned columns in the admin dashboard "blog" table.
    # 'category__name', 'author__name' are foreign keys so to search we have provide the field name with the column ex:- " 'category__name', 'author__name' "
    search_fields = ['title', 'category__name', 'author__username', 'status', 'is_featured'] # provide search to get matching datasets in admin dashboard.
    list_editable = ['status', 'is_featured'] # make these fields editable in the list view in the admin dashboard.


# Register your models here.
admin.site.register(Category)
admin.site.register(Blog, SlugAdmin)
admin.site.register(About)
admin.site.register(SocialLinks)