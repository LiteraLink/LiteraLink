# Generated by Django 4.2.6 on 2023-10-28 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0020_alter_forumreply_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumreply',
            name='timestamp',
            field=models.CharField(default='2023-10-28', max_length=255),
        ),
    ]
