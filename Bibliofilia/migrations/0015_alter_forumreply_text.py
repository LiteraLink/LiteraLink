# Generated by Django 4.2.6 on 2023-10-28 04:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0014_alter_forum_userreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumreply',
            name='text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]