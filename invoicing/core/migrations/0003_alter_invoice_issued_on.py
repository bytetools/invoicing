# Generated by Django 4.0.4 on 2022-05-02 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_invoice_issued_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='issued_on',
            field=models.DateField(),
        ),
    ]
