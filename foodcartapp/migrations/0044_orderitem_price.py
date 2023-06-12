# Generated by Django 3.2.15 on 2023-06-12 04:25

from django.db import migrations, models
import foodcartapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=6, validators=[foodcartapp.models.validate_positive], verbose_name='Цена'),
            preserve_default=False,
        ),
    ]