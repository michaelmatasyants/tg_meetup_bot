# Generated by Django 4.2.2 on 2023-06-24 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_report_actual_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
