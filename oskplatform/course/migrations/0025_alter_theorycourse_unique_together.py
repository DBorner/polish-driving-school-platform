# Generated by Django 4.2.1 on 2023-06-05 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_qualification_date_of_achievement_lte_today_and_more'),
        ('course', '0024_remove_theorycourse_start_date_gte_today_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='theorycourse',
            unique_together={('start_date', 'type', 'instructor')},
        ),
    ]
