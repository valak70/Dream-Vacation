# Generated by Django 5.1.4 on 2025-01-03 15:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='upvoted_by',
            field=models.ManyToManyField(blank=True, related_name='upvoted_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]