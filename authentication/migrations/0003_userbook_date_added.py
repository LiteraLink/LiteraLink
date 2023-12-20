# Generated by Django 4.2.6 on 2023-12-20 04:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_userbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbook',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
