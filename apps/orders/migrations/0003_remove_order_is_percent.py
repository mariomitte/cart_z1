# Generated by Django 3.1.3 on 2020-11-19 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_is_percent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='is_percent',
        ),
    ]
