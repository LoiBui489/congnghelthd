# Generated by Django 5.0 on 2024-02-19 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0011_alter_myorderproduct_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='shipping_fee',
            field=models.IntegerField(default=0),
        ),
    ]
