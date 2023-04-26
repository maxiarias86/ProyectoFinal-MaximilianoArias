# Generated by Django 4.1.7 on 2023-04-26 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AppCuentos', '0003_cuento_foto_delete_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuento',
            name='foto',
        ),
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos')),
                ('cuento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AppCuentos.cuento')),
            ],
        ),
    ]