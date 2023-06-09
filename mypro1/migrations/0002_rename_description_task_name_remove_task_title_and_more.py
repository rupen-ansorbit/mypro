# Generated by Django 4.1.9 on 2023-06-09 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypro1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='description',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='Pending', max_length=100),
        ),
    ]