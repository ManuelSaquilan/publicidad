# Generated by Django 4.2.14 on 2024-09-02 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publiApp', '0005_customsession_last_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customsession',
            name='session_key',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
