# Generated by Django 3.2.5 on 2021-09-20 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_bill_descriptionofgoods'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='shipingMark',
            field=models.TextField(default='1 - <django.db.models.fields.IntegerField> <django.db.models.fields.TextField>'),
        ),
    ]