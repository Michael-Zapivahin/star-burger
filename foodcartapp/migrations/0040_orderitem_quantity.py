# Generated by Django 3.2.15 on 2023-06-09 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0039_alter_order_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='Количество'),
            preserve_default=False,
        ),
    ]
