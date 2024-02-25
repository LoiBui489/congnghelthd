# Generated by Django 5.0 on 2024-01-17 09:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.BigIntegerField(default=100000),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='MyOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('product_price', models.BigIntegerField()),
                ('quantity', models.SmallIntegerField(default=1)),
                ('user_request', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('status', models.CharField(max_length=10)),
                ('shipping_address', models.CharField(max_length=200)),
                ('shipping_fee', models.BigIntegerField(default=0)),
                ('total_fee', models.BigIntegerField()),
                ('payed', models.BigIntegerField(default=0, null=True)),
                ('pay_by', models.CharField(max_length=10)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.department')),
                ('ordered_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('products', models.ManyToManyField(related_name='orders', through='exam.MyOrderProduct', to='exam.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='myorderproduct',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exam.order'),
        ),
    ]