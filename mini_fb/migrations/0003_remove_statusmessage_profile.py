# Generated by Django 5.1.1 on 2024-10-14 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0002_rename_indexes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statusmessage',
            name='profile',
        ),
    ]