# Generated by Django 5.0.6 on 2024-06-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_ogloszenie_is_reserved_alter_zdjecie_dane'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezerwacja',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
