# Generated by Django 4.0.1 on 2022-01-20 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jackshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
    ]
