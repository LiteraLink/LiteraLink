# Generated by Django 4.2.6 on 2023-10-25 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bibliofilia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='userReview',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='forum',
            name='BookName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='forum',
            name='forumsDescription',
            field=models.CharField(max_length=255),
        ),
    ]