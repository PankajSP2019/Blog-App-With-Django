from django.contrib import admin
from .models import Post, BlogComment

# Register your models here.
admin.site.register(Post)
admin.site.register(BlogComment)

# We Can Also Pass By In A Tuple
# admin.site.register(Post, BlogComment)