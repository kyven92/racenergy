# Generated by Django 2.2.10 on 2020-02-06 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racIOT', '0009_auto_20200206_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rps_data',
            name='entry_id',
            field=models.IntegerField(db_index=True, default=-1),
        ),
    ]
