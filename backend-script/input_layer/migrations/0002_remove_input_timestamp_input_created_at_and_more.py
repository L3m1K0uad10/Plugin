# Generated by Django 4.2 on 2024-12-21 08:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('input_layer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='input',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='input',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
