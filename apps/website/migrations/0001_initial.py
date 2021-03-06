# Generated by Django 3.1.3 on 2020-11-18 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('logo', models.ImageField(upload_to='website')),
                ('header_image', models.ImageField(upload_to='website')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('website', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
            ],
            options={
                'verbose_name': 'website',
                'verbose_name_plural': 'websites',
                'ordering': ('-created',),
            },
        ),
    ]
