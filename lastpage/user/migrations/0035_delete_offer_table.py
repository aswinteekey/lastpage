# Generated by Django 5.0.4 on 2024-05-13 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_offer_table_post_suggest_table_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='offer_table',
        ),
    ]