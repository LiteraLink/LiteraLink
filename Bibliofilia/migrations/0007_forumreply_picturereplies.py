# Generated by Django 4.2.6 on 2023-10-27 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0006_forumreply'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumreply',
            name='pictureReplies',
            field=models.ImageField(default=1, upload_to='reviewimages/'),
            preserve_default=False,
        ),
    ]