# Generated by Django 4.2.6 on 2023-10-29 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_userbook'),
        ('BacaDiTempat', '0008_remove_venue_book_amount_venue_rent_book_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookvenue',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.userprofile'),
        ),
    ]
