# Generated by Django 4.0.3 on 2022-04-11 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='description',
            field=models.CharField(default=0, editable=False, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='issued_on',
            field=models.DateField(auto_now=True),
        ),
    ]