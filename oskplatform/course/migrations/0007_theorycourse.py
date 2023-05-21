# Generated by Django 4.2.1 on 2023-05-21 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_employee'),
        ('course', '0006_alter_course_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='TheoryCourse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('T', 'Tygodniowy'), ('W', 'Weekendowy')], default='T', max_length=1)),
                ('start_date', models.DateField()),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.instructor')),
            ],
        ),
    ]
