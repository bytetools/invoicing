# Generated by Django 4.0.4 on 2022-05-02 19:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='issued_on',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
