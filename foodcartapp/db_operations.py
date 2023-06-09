
from foodcartapp.models import Order, OrderItem, Product
from django.shortcuts import get_object_or_404


def create_order(order_content):
    order, created = Order.objects.update_or_create(
        phone_number=order_content['phonenumber'],
        defaults={
            'name': order_content['firstname'],
            'surname': order_content['lastname'],
            'address': order_content['address'],
        }
    )

    for index, product_key in enumerate(order_content['products']):
        product = get_object_or_404(Product, pk=int(product_key['product']))
        item = OrderItem.objects.update_or_create(
            order=order,
            product=product,
            defaults={
                'quantity': product_key['quantity'],
            }
        )
    return order
