# Generated by Django 4.2.11 on 2024-04-13 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_remove_post_user_post_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='username',
        ),
    ]