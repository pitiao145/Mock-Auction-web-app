# Generated by Django 4.2.5 on 2023-10-13 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0004_rename_bids_bid_rename_comments_comment_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="listing",
            old_name="price",
            new_name="starting_bid",
        ),
        migrations.AlterField(
            model_name="bid",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="auctions.listing",
            ),
        ),
        migrations.AlterField(
            model_name="bid",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bidders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="auctions.listing",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="commenters",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
