# Generated by Django 5.0.6 on 2024-06-25 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to='auctions.listing'),
        ),
    ]
