# Generated by Django 4.2.7 on 2023-12-16 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0026_alter_forum_bookname_alter_forum_forumsdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='bookPicture',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]