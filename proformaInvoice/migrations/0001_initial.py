# Generated by Django 3.2.5 on 2021-09-16 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProformaInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proformaInvoice', models.TextField()),
                ('proformaDate', models.DateField()),
                ('otherReferences', models.TextField(blank=True, null=True)),
                ('termsOfPayment', models.TextField(blank=True, null=True)),
                ('deliveryTerms', models.TextField(blank=True, null=True)),
                ('preCarriage', models.TextField(blank=True, null=True)),
                ('vesselFlightNo', models.TextField(blank=True, null=True)),
                ('placeOfReceipt', models.TextField(blank=True, null=True)),
                ('portOfLoading', models.TextField(blank=True, null=True)),
                ('portOfDischarge', models.TextField(blank=True, null=True)),
                ('finalDestination', models.TextField(blank=True, null=True)),
                ('products', models.TextField()),
                ('currency', models.TextField()),
                ('totalSales', models.TextField()),
                ('customerId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company')),
            ],
        ),
    ]
