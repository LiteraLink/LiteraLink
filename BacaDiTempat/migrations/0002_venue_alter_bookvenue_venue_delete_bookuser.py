# Generated by Django 4.2.6 on 2023-10-27 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BacaDiTempat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('address', models.TextField()),
                ('venue_open', models.CharField(max_length=50)),
                ('book_amount', models.IntegerField()),
                ('date_use', models.DateField(auto_now_add=True)),
                ('date_return', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='bookvenue',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BacaDiTempat.venue'),
        ),
        migrations.DeleteModel(
            name='BookUser',
        ),
    ]
