# Generated by Django 3.1.3 on 2020-11-19 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_percent',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]