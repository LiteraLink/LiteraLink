# Generated by Django 4.2.6 on 2023-10-27 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0010_forumreply_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumreply',
            name='parent_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
