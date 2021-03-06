# Generated by Django 2.1.1 on 2020-08-01 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeterUsage',
            fields=[
                ('meter_id', models.IntegerField(primary_key=True, serialize=False)),
                ('read_month', models.IntegerField()),
                ('read_year', models.IntegerField()),
                ('min_kwh', models.DecimalField(decimal_places=4, max_digits=19)),
                ('max_kwh', models.DecimalField(decimal_places=4, max_digits=19)),
                ('total_usage', models.DecimalField(decimal_places=4, max_digits=19)),
            ],
            options={
                'db_table': 'vw_meter_usage',
                'managed': False,
            },
        ),
    ]
