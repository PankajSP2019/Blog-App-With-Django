# Generated by Django 4.2.11 on 2024-04-13 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0023_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, choices=[('Tech', 'Tech'), ('Life Style', 'Life Style'), ('Fitness Focus', 'Fitness Focus'), ('Bookworm Corner', 'Bookworm Corner'), ('Digital Insights', 'Digital Insights'), ('Creative Crafts', 'Creative Crafts'), ('Travel Tales', 'Travel Tales'), ('Inspirational Stories ', 'Inspirational Stories')], max_length=100),
        ),
    ]
