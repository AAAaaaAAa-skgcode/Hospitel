# Generated by Django 3.2 on 2021-05-17 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_remove_hospital_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccine',
            name='brand',
            field=models.CharField(blank=True, choices=[('Pfizer', 'Pfizer'), ('AstraZeneca', 'AstraZeneca'), ('Moderna', 'Moderna'), ('Johnson & Johnson', 'Johnson & Johnson')], default='', max_length=200, null=True),
        ),
    ]