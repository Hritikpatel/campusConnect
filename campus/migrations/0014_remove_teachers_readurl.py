# Generated by Django 4.1 on 2023-03-20 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0013_attendancesheets_delete_attendance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teachers',
            name='readUrl',
        ),
    ]
