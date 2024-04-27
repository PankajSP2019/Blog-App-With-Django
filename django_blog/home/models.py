from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.

class Contact_H(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"CID-{self.sno} Name-{self.name}"


# For user profile
class UserProfile(models.Model):
    up_no = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # dob = models.DateField()
    # address = models.TextField(max_length=500)
    profile_picture = models.ImageField(upload_to="home/user_image")
    is_author = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile ID-{self.up_no} UserName-{self.user.username} Is_Author-{self.is_author}"


class AuthorRequest(models.Model):
    CATEGORY_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),

    ]

    ar_no = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    about_author = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    reject_reason = models.TextField(blank=True)

    # If the Status is Rejected once It Cannot Be Changed
    # def save(self, *args, **kwargs):
    #     if self.pk:  # Check if the instance has already been saved (i.e., is not a new instance)
    #         original_status = AuthorRequest.objects.get(pk=self.pk).status
    #         if original_status == 'Rejected' and self.status != 'Rejected':
    #             # If the status is already Rejected and trying to change it, raise an exception
    #             raise ValueError("Cannot change status from 'Rejected'.")
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Request-No:{self.ar_no} User:{self.user} Status:{self.status}"
