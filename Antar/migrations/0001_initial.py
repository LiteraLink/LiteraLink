# Generated by Django 4.2.6 on 2023-10-25 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_lengkap', models.CharField(max_length=255)),
                ('nomor_telepon', models.CharField(max_length=255)),
                ('alamat_pengiriman', models.TextField()),
                ('nama_buku_dipesan', models.CharField(max_length=100)),
                ('jumlah_buku_dipesan', models.IntegerField()),
                ('durasi_peminjaman', models.IntegerField()),
                ('total_payment', models.CharField(max_length=255)),
                ('tanggal_pengiriman', models.DateField(auto_now_add=True)),
                ('waktu_pengiriman', models.DurationField()),
                ('status_pesanan', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookID', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('authors', models.CharField(max_length=255)),
                ('display_authors', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('categories', models.CharField(max_length=255)),
                ('thumbnail', models.TextField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Antar.person')),
            ],
        ),
    ]
