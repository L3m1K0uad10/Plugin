# Generated by Django 4.2 on 2025-01-15 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('code', models.TextField(blank=True)),
            ],
        ),
    ]
