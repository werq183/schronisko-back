# Generated by Django 5.0.6 on 2024-06-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_rezerwacja_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ogloszenie',
            name='data',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
