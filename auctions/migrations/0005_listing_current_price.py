# Generated by Django 4.1.1 on 2023-04-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="current_price",
            field=models.IntegerField(default=0),
        ),
    ]
