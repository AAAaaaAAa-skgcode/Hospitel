# Generated by Django 3.2 on 2021-04-27 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='address',
        ),
    ]
