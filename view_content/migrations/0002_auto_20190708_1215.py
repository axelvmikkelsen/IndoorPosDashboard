# Generated by Django 2.2.3 on 2019-07-08 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='port',
            field=models.PositiveIntegerField(),
        ),
    ]
