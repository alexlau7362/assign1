# Generated by Django 4.2.19 on 2025-04-07 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product',
            new_name='name',
        ),
    ]
