# Generated by Django 4.1.4 on 2024-03-15 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('tech', 'Tech'), ('lifestyle', 'Life Style'), ('fitness focus', 'Fitness Focus'), ('bookworm corner', 'Bookworm Corner'), ('digital insights', 'Digital Insights'), ('creative crafts', 'Creative Crafts'), ('travel tales', 'Travel Tales'), ('inspirational stories', 'Inspirational Stories')], default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateField(blank=True),
        ),
    ]
