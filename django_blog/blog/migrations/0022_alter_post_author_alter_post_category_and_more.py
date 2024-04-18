# Generated by Django 4.2.11 on 2024-04-13 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0021_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, choices=[('Tech', 'Tech'), ('Life Style', 'Life Style'), ('Fitness Focus', 'Fitness Focus'), ('Bookworm Corner', 'Bookworm Corner'), ('Digital Insights', 'Digital Insights'), ('Creative Crafts', 'Creative Crafts'), ('Travel Tales', 'Travel Tales'), ('m ', 'Inspirational Stories')], max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
        ),
    ]