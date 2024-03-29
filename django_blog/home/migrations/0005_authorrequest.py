# Generated by Django 4.2.11 on 2024-03-29 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0004_remove_userprofile_address_remove_userprofile_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorRequest',
            fields=[
                ('ar_no', models.AutoField(primary_key=True, serialize=False)),
                ('about_author', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
