# Generated by Django 4.2.6 on 2023-10-27 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BacaDiTempat', '0003_remove_venue_name_venue_book_name_venue_person_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='place_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]