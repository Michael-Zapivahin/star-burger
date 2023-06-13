# Generated by Django 3.2.15 on 2023-06-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('CASH', 'Наличными'), ('CARD', 'Картой')], db_index=True, default='CASH', max_length=15, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('01', 'Не обработан'), ('02', 'Готовится'), ('03', 'Доставка'), ('04', 'Доставлен')], db_index=True, default='01', max_length=15, verbose_name='Статус'),
        ),
    ]