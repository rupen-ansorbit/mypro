# Generated by Django 4.1.9 on 2023-06-09 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypro1', '0004_alter_user_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
