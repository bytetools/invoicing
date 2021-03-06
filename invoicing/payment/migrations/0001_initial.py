# Generated by Django 4.0.1 on 2022-05-07 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HelcimDebitTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('token', models.CharField(max_length=32)),
                ('test', models.BooleanField(default=False)),
                ('amount', models.FloatField()),
                ('response', models.BooleanField()),
                ('response_message', models.CharField(max_length=12)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('notice_message', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=16)),
                ('transaction_id', models.CharField(max_length=12)),
                ('order_number', models.CharField(max_length=12)),
                ('customer_code', models.CharField(max_length=8)),
                ('currency', models.CharField(max_length=3)),
                ('bank_account_type', models.CharField(choices=[('CHK', 'Chequing'), ('SAV', 'Savings')], max_length=3)),
                ('bank_account_corporate', models.CharField(choices=[('P', 'Personal'), ('C', 'Corporate')], max_length=1)),
                ('bank_account_token', models.CharField(max_length=12)),
                ('bank_financial_number', models.CharField(max_length=8)),
                ('bank_transit_number', models.CharField(max_length=8)),
                ('bank_account_number', models.CharField(max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='debit_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HelcimCreditTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('token', models.CharField(max_length=32)),
                ('test', models.BooleanField(default=False)),
                ('amount', models.FloatField()),
                ('response', models.BooleanField()),
                ('response_message', models.CharField(max_length=12)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('notice_message', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=16)),
                ('transaction_id', models.CharField(max_length=12)),
                ('order_number', models.CharField(max_length=12)),
                ('customer_code', models.CharField(max_length=8)),
                ('currency', models.CharField(max_length=3)),
                ('card_holder_name', models.CharField(max_length=32)),
                ('card_holder_address', models.CharField(max_length=32)),
                ('card_holder_postal_code', models.CharField(max_length=8)),
                ('card_number', models.CharField(max_length=22)),
                ('avs_response', models.CharField(max_length=1)),
                ('cvv_response', models.CharField(max_length=1)),
                ('approval_code', models.CharField(max_length=12)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='credit_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
