# Generated by Django 5.0.4 on 2024-06-05 09:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_listtable_quantity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='listtable',
            name='fadvertisement_id',
            field=models.ForeignKey(db_column='fadvertisement_id', on_delete=django.db.models.deletion.CASCADE, to='home.hometable'),
        ),
        migrations.AlterField(
            model_name='listtable',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
