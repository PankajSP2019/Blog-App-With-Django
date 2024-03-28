from django.db import models
from django.contrib.auth.models import User


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

    def __str__(self):
        return f"Profile ID-{self.up_no} UserName-{self.user.username}"


