# Generated by Django 3.1.1 on 2020-09-27 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdeye', '0003_camera_node_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='rtl',
            field=models.BooleanField(default=True),
        ),
    ]
