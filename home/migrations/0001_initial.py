# Generated by Django 5.0.4 on 2024-05-31 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomeTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('marketingtype', models.CharField(max_length=100)),
                ('pricerange', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='image')),
            ],
        ),
    ]
