# Generated by Django 4.2.17 on 2025-01-10 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='contact_shared',
            field=models.BooleanField(default=False),
        ),
    ]
