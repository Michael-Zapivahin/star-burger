

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from foodcartapp.models import Order, OrderItem, Product
from django.shortcuts import get_object_or_404

import foodcartapp.db_operations as db


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        # order_content = get_text()
        # print(str(order_content))

        orders = []
        for order in Order.objects.all().get_order_cost():
            orders.append(
                {
                    "firstname": order.firstname,
                    "lastname": order.lastname,
                    "phonenumber": order.phonenumber,
                    "address": order.phonenumber,
                    "id": order.id,
                    "cost": order.cost,
                }
            )
            print(orders)
            break




def get_text():
    return {
        "products": [{"product": 3, "quantity": 1}, {"product": 5, "quantity": 2}],
        "firstname": "Michael",
        "lastname": "Zapivahin",
        "phonenumber": "+79778108747",
        "address": "Красногорск Лесная 5"
    }

