# Generated by Django 4.2.3 on 2024-04-19 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolSystem', '0005_remove_item_user_type_alter_item_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='type',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
    ]
