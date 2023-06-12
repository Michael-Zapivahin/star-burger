
from foodcartapp.models import Order, OrderItem, Product
from geodata.models import Place
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.urls import reverse


def create_place(place_content):
    place, created = Place.objects.update_or_create(
        lat=place_content['lat'],
        lon=place_content['lon'],
        place=place_content['place'],
    )
    return place


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

    for _, order_item in enumerate(order_content['products']):
        product = get_object_or_404(Product, pk=order_item['product'])
        _ = OrderItem.objects.update_or_create(
            order=order,
            product=product,
            defaults={
                'quantity': order_item['quantity'],
                'price': product.price,
            },
        )
    return order


def get_orders():
    orders = []
    for order in Order.objects.filter(status__in=['Готовится', 'Необработан']).get_order_cost():
        orders.append(
            {
                "firstname": order.firstname,
                "lastname": order.lastname,
                "phonenumber": order.phonenumber,
                "address": order.address,
                "id": order.id,
                "cost": order.cost,
                "status": order.status,
                "comment": order.comment or '',
                "payment": order.payment,
                "admin_url": reverse('admin:foodcartapp_order_change', args=(order.id,))
            }
        )
    return orders
