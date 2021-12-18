# Generated by Django 3.2.9 on 2021-12-05 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin1_void1', models.FloatField()),
                ('pin1_fuel', models.FloatField()),
                ('pin1_void2', models.FloatField()),
                ('pin1_clad', models.FloatField()),
                ('pin2_termfuel', models.FloatField()),
                ('pin2_clad', models.FloatField()),
            ],
        ),
    ]
