# Generated by Django 4.1.1 on 2022-09-23 10:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_alter_rooms_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='participants',
            field=models.ManyToManyField(blank='True', related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
    ]