
from foodcartapp.models import Order, OrderItem, Product
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer

class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(ModelSerializer):

    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'firstname', 'lastname', 'phonenumber', 'address', 'products']


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
