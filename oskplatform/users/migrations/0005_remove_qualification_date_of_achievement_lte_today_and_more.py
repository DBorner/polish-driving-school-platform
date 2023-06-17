# Generated by Django 4.2.1 on 2023-06-17 18:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_qualification_date_of_achievement_lte_today_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='qualification',
            name='date_of_achievement_lte_today',
        ),
        migrations.AddConstraint(
            model_name='qualification',
            constraint=models.CheckConstraint(check=models.Q(('date_of_achievement__lte', datetime.date(2023, 6, 17))), name='date_of_achievement_lte_today'),
        ),
    ]
