from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# from tinymce.models import HTMLField

# For Custom Template Tags
from .templatetags import extras


# Create your models here.

class Post(models.Model):
    # For Category Choice Field
    CATEGORY_CHOICES = [
        ('Tech', 'Tech'),
        ('Life Style', 'Life Style'),
        ('Fitness Focus', 'Fitness Focus'),
        ('Bookworm Corner', 'Bookworm Corner'),
        ('Digital Insights', 'Digital Insights'),
        ('Creative Crafts', 'Creative Crafts'),
        ('Travel Tales', 'Travel Tales'),
        ('Inspirational Stories ', 'Inspirational Stories')
    ]

    pno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, blank=True, choices=CATEGORY_CHOICES)
    slug = models.CharField(max_length=700, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    content = models.TextField()
    summary = models.TextField()
    image = models.ImageField(upload_to="blog/images", default="")
    last_edit = models.DateTimeField(blank=True, null=True)

    # For Automatic save the slug from title
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"(PostID - {self.pno}) - (Title - {self.title})"


# For Commenting In The Comment

class BlogComment(models.Model):
    cno = models.AutoField(primary_key=True)
    comment = models.TextField(max_length=500)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # If the User is deleted , related comment will also delete
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"(CID - {self.cno} PostID - {self.post.pno}) - (user - {self.user.username})  comment - {self.comment[:50]}"
