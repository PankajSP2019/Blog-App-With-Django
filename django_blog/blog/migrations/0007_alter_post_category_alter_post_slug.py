# Generated by Django 4.1.4 on 2024-03-15 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(blank=True, choices=[('tech', 'Tech'), ('lifestyle', 'Life Style'), ('fitness focus', 'Fitness Focus'), ('bookworm corner', 'Bookworm Corner'), ('digital insights', 'Digital Insights'), ('creative crafts', 'Creative Crafts'), ('travel tales', 'Travel Tales'), ('inspirational stories', 'Inspirational Stories')], default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.CharField(blank=True, max_length=700, null=True),
        ),
    ]
