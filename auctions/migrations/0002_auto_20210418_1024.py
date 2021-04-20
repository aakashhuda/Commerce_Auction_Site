# Generated by Django 3.1.7 on 2021-04-18 10:24

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='BDT', max_digits=19),
        ),
    ]
