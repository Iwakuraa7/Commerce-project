# Generated by Django 5.0.6 on 2024-06-23 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_highest_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
