# Generated by Django 5.0.4 on 2024-04-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_book_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_table',
            name='book_id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
