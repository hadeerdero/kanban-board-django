# Generated by Django 5.1.6 on 2025-02-09 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stage',
            options={},
        ),
        migrations.RemoveField(
            model_name='stage',
            name='order',
        ),
    ]
