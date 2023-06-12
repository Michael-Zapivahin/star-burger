
from foodcartapp.models import Order, OrderItem, Product
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer
from django.db import transaction


@transaction.atomic
def create_order(order_content):
    order, created = Order.objects.update_or_create(
        phonenumber=order_content['phonenumber'],
        defaults={
            'firstname': order_content['firstname'],
            'lastname': order_content['lastname'],
            'address': order_content['address'],
        }
    )

    for index, product_key in enumerate(order_content['products']):
        product = get_object_or_404(Product, pk=product_key['product'])
        item = OrderItem.objects.update_or_create(
            order=order,
            # product=product_key['product'],
            product=product,
            defaults={
                'quantity': product_key['quantity'],
            },
            price=product.price
        )
    return order


def get_orders():
    orders = []
    for order in Order.objects.all().get_order_cost():
        orders.append(
            {
                "firstname": order.firstname,
                "lastname": order.lastname,
                "phonenumber": order.phonenumber,
                "address": order.address,
                "id": order.id,
                "cost": order.cost,
            }
        )
    return orders
