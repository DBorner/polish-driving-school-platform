# Generated by Django 4.2.1 on 2023-05-22 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_category_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
    ]
