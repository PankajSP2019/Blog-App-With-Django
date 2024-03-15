from django.db import models


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
        ('Inspirational Stories', 'Inspirational Stories')
    ]

    pno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True, choices=CATEGORY_CHOICES)
    slug = models.CharField(max_length=700, blank=True, null=True)
    timestamp = models.DateField(blank=True)
    content = models.TextField()
    summary = models.CharField(max_length=500)
    image = models.ImageField(upload_to="blog/images", default="")

    # For Automatic save the slug from title
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"(PostID - {self.pno}) - (Title - {self.title})"
