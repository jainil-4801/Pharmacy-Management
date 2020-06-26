# Generated by Django 3.0.6 on 2020-05-22 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=11)),
                ('Name', models.CharField(max_length=50)),
                ('Quantity', models.IntegerField()),
                ('QuickView', models.CharField(max_length=10000)),
            ],
        ),
    ]