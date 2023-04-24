# Generated by Django 4.2 on 2023-04-19 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_item_image_alter_item_category_alter_item_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ForeignKey(default='item', on_delete=django.db.models.deletion.CASCADE, to='catalog.item'),
            preserve_default=False,
        ),
    ]
