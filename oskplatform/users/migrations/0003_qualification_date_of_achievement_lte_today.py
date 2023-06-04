# Generated by Django 4.2.1 on 2023-06-04 20:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_qualification_unique_together'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='qualification',
            constraint=models.CheckConstraint(check=models.Q(('date_of_achievement__lte', datetime.date(2023, 6, 4))), name='date_of_achievement_lte_today'),
        ),
    ]