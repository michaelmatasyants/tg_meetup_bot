# Generated by Django 4.2.2 on 2023-06-23 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_user_tg_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tg_nickname',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
