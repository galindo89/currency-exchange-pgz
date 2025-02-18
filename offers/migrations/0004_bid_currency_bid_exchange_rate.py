# Generated by Django 4.2.17 on 2025-01-15 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_alter_offer_exchange_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro')], default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bid',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=8),
            preserve_default=False,
        ),
    ]
