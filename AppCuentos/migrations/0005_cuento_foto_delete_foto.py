# Generated by Django 4.1.7 on 2023-04-26 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCuentos', '0004_remove_cuento_foto_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuento',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos'),
        ),
        migrations.DeleteModel(
            name='Foto',
        ),
    ]