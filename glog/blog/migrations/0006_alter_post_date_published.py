# Generated by Django 4.1 on 2023-01-28 00:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_managers_alter_post_date_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_published',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 28, 0, 7, 3, 203036, tzinfo=datetime.timezone.utc)),
        ),
    ]