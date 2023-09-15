# Generated by Django 4.1.1 on 2023-04-12 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0014_listing_datetime_alter_listing_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bid",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="auctions.listing",
            ),
        ),
    ]