# Generated by Django 3.2.2 on 2024-03-17 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location_x',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location_y',
            field=models.TextField(blank=True),
        ),
    ]
