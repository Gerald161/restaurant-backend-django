# Generated by Django 4.2.5 on 2023-09-11 15:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_resettoken_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resettoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 11, 16, 19, 33, 667002, tzinfo=datetime.timezone.utc)),
        ),
    ]
