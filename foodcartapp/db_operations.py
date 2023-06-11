
from foodcartapp.models import Order, OrderItem, Product
from django.shortcuts import get_object_or_404


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
        item = OrderItem.objects.update_or_create(
            order=order,
            product=product_key['product'],
            defaults={
                'quantity': product_key['quantity'],
            }
        )
    return order
