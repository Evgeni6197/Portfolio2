# Generated by Django 4.1.1 on 2023-04-09 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0007_watchlist_delete_user1"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="status",
            field=models.CharField(
                choices=[("r", "regular"), ("w", "winner")], default="r", max_length=1
            ),
        ),
    ]
