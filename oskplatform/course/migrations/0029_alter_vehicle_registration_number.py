# Generated by Django 4.2.1 on 2023-06-19 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0028_remove_vehicle_year_lte_current_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='registration_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
