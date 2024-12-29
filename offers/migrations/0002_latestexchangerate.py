# Generated by Django 4.2.17 on 2024-12-27 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LatestExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(default='USD', max_length=3)),
                ('target_currency', models.CharField(default='EUR', max_length=3)),
                ('rate', models.DecimalField(decimal_places=6, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
