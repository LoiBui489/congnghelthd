# Generated by Django 5.0 on 2024-02-19 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_department_manager_comment_follow_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(default='371 Nguyen Kiem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(default='ROLE_USER', max_length=10),
        ),
    ]
