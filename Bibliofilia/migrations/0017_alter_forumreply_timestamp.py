# Generated by Django 4.2.6 on 2023-10-28 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0016_alter_forumreply_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumreply',
            name='timestamp',
            field=models.DateTimeField(default='2023-10-28 10:27:20'),
        ),
    ]
