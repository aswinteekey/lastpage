# Generated by Django 5.0.4 on 2024-04-25 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_remove_exchange_table_readshare_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='collect_point',
            name='coll_pw',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
