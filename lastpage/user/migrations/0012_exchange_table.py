# Generated by Django 5.0.4 on 2024-04-18 13:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_book_table_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='exchange_table',
            fields=[
                ('exc_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=10)),
                ('otp', models.IntegerField(blank=True, null=True)),
                ('readshare_status', models.CharField(max_length=10)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.book_table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.pageuser')),
            ],
        ),
    ]