# Generated by Django 4.0.1 on 2022-01-20 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jackshop', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(null=True),
        ),
    ]