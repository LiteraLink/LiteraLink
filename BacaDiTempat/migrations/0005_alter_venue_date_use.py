# Generated by Django 4.2.6 on 2023-10-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BacaDiTempat', '0004_venue_place_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='date_use',
            field=models.DateField(blank=True, null=True),
        ),
    ]
