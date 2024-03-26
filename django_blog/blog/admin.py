from django.contrib import admin
from .models import Post, BlogComment
from django.forms import Textarea
from django.db import models

# Register your models here.
# admin.site.register(Post)
admin.site.register(BlogComment)

# admin.site.register(Post)


# We Can Also Pass By In A Tuple
# admin.site.register(Post, BlogComment)


class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/tinyInject.js',)  # Path to your JavaScript file

    # formfield_overrides = {
    #     models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 120})},  # Adjust rows and cols as needed
    # }

admin.site.register(Post, PostAdmin)
