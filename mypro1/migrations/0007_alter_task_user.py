# Generated by Django 4.1.9 on 2023-06-09 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypro1', '0006_alter_task_created_at_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.CharField(max_length=50),
        ),
    ]
