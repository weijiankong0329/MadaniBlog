# Generated by Django 4.2.1 on 2023-06-18 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_blogger_follower'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='label_tag',
            new_name='label_category',
        ),
    ]
