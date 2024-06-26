# Generated by Django 4.2.11 on 2024-03-28 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_rename_contact_contact_h'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('up_no', models.AutoField(primary_key=True, serialize=False)),
                ('dob', models.DateField()),
                ('address', models.TextField(max_length=500)),
                ('profile_picture', models.ImageField(upload_to='home/user_image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
