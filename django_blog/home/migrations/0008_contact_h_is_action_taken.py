# Generated by Django 4.2.11 on 2024-06-03 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_authorrequest_reject_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_h',
            name='is_action_taken',
            field=models.BooleanField(default=False),
        ),
    ]