# Generated by Django 4.2.6 on 2023-10-28 02:38

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0013_forum_repliestotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='userReview',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]