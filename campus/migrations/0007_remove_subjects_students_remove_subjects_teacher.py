# Generated by Django 4.1 on 2023-03-11 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0006_alter_todo_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='students',
        ),
        migrations.RemoveField(
            model_name='subjects',
            name='teacher',
        ),
    ]
