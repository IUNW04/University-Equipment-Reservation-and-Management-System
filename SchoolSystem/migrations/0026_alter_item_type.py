# Generated by Django 4.2.3 on 2024-04-20 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SchoolSystem', '0025_alter_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
