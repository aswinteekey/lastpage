# Generated by Django 5.0.4 on 2024-04-25 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_collect_point_coll_pw'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange_table',
            name='rej_in_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='exchange_table',
            name='rej_out_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
