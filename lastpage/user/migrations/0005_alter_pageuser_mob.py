# Generated by Django 5.0.4 on 2024-04-07 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_rename_user_table_pageuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageuser',
            name='mob',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
