# Generated by Django 5.0.4 on 2024-06-01 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_listtable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listtable',
            old_name='product_id',
            new_name='fadvertisement_id',
        ),
    ]
