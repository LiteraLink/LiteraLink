# Generated by Django 4.2.6 on 2023-10-26 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Bibliofilia', '0005_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Bibliofilia.forum')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
