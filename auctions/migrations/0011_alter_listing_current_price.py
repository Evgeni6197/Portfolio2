# Generated by Django 4.1.1 on 2023-04-12 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_rename_comment_comment_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="current_price",
            field=models.IntegerField(default=models.F("starting_bid")),
        ),
    ]
