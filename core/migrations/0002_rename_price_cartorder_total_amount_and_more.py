# Generated by Django 5.0 on 2024-01-08 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartorder',
            old_name='price',
            new_name='total_amount',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address2',
        ),
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]