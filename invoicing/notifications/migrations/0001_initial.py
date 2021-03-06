# Generated by Django 4.0.1 on 2022-05-16 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_alter_product_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('bcc_recipients', models.ManyToManyField(blank=True, related_name='email_attempted_bcc_to', to=settings.AUTH_USER_MODEL)),
                ('cc_recipients', models.ManyToManyField(blank=True, related_name='emails_attempted_cc_to', to=settings.AUTH_USER_MODEL)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='email_attempts', to='core.invoice')),
                ('recipients', models.ManyToManyField(blank=True, related_name='emails_attempted_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
