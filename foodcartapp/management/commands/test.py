

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from foodcartapp.models import Order, OrderItem, Product
from django.shortcuts import get_object_or_404

import foodcartapp.db_operations as db


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        order_content = get_text()
        order = db.create_order(order_content)
        print(str(order))
        # order, created = Order.objects.update_or_create(
        #     phone_number=order_content['phonenumber'],
        #     defaults={
        #         'name': order_content['firstname'],
        #         'surname': order_content['lastname'],
        #         'address': order_content['address'],
        #     }
        # )
        #
        # for index, product_key in enumerate(order_content['products']):
        #     product = get_object_or_404(Product, pk=int(product_key['product']))
        #     item = OrderItem.objects.update_or_create(
        #         order=order,
        #         product=product,
        #         defaults={
        #             'quantity': product_key['quantity'],
        #         }
        #     )



def get_text():
    return {
        'products': [{'product': 3, 'quantity': 1}, {'product': 5, 'quantity': 2}],
        'firstname': 'Michael',
        'lastname': 'Zapivahin',
        'phonenumber': '+7977808747',
        'address': 'Красногорск улица Лесная дом 5'
    }

