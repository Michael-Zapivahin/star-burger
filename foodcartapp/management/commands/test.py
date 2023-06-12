

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from foodcartapp.models import Order, OrderItem, Product
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer

import foodcartapp.db_operations as db


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(ModelSerializer):

    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        order_content = get_text()
        serializer = OrderSerializer(data=order_content)
        serializer.is_valid(raise_exception=True)
        order = db.create_order(order_content)
        serializer = OrderSerializer(order)
        print(serializer.data)


        # order, created = Order.objects.update_or_create(
        #     phonenumber=order_content['phonenumber'],
        #     defaults={
        #         'firstname': order_content['firstname'],
        #         'lastname': order_content['lastname'],
        #         'address': order_content['address'],
        #     }
        # )
        #
        # for index, product_key in enumerate(order_content['products']):
        #     product = get_object_or_404(Product, pk=product_key['product'])
        #     item = OrderItem.objects.update_or_create(
        #         order=order,
        #         # product=product_key['product'],
        #         product=product,
        #         defaults={
        #             'quantity': product_key['quantity'],
        #         },
        #         price=product.price
        #     )






def get_text():
    return {
        "products": [{"product": 3, "quantity": 1}, {"product": 5, "quantity": 2}],
        "firstname": "Michael",
        "lastname": "Zapivahin",
        "phonenumber": "+79778108745",
        "address": "Красногорск Лесная 5"
    }

