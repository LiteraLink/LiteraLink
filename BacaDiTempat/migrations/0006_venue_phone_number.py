# Generated by Django 4.2.6 on 2023-10-27 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BacaDiTempat', '0005_alter_venue_date_use'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='phone_number',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]