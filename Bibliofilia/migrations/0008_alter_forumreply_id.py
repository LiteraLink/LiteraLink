# Generated by Django 4.2.6 on 2023-10-27 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0007_forumreply_picturereplies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumreply',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
