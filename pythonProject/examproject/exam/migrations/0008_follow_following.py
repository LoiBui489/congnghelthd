# Generated by Django 5.0 on 2024-02-19 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0007_department_map_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.BooleanField(default=False),
        ),
    ]
