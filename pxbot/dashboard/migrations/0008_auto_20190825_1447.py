# Generated by Django 2.2.4 on 2019-08-25 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20190825_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(),
        ),
    ]
