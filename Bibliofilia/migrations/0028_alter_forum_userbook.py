# Generated by Django 4.2.7 on 2023-12-16 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_book_display_authors'),
        ('Bibliofilia', '0027_alter_forum_bookpicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='userbook',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.book'),
        ),
    ]
