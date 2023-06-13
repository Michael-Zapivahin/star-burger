
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from foodcartapp.models import Order, OrderItem, Product, RestaurantMenuItem, Restaurant
from django.shortcuts import get_object_or_404
from rest_framework.serializers import ModelSerializer

import foodcartapp.db_operations as db

import star_burger.settings as settings


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
        test_function()


def test_function():
    orders = list(Order.objects.exclude(status=Order.DONE).get_order_cost().order_by('status'))
    menu_items = RestaurantMenuItem.objects.filter(availability=True).values('restaurant', 'product')
    restaurants = {}
    for item in menu_items:
        restaurants[f'restaurant_{item["restaurant"]}'] = get_object_or_404(Restaurant, pk=item["restaurant"])
    for order in orders:
        if order.restaurant is None:
            order_restaurants = []
            order_products = order.products.all()
            for restaurant in restaurants:
                restaurants_possible = True
                for order_product in order_products:
                    restaurants_for_product = menu_items.filter(product=order_product.product,
                                                                restaurant=restaurants[restaurant])
                    if not restaurants_for_product:
                        restaurants_possible = False
                if restaurants_possible:
                    order_restaurants.append(restaurants[restaurant])

            if order_restaurants:
                order.restaurant_selected = order_restaurants[0].name
        else:
            order.restaurant_selected = order.restaurant.name



def get_text():
    return {
        "products": [{"product": 3, "quantity": 1}, {"product": 5, "quantity": 2}],
        "firstname": "Michael",
        "lastname": "Zapivahin",
        "phonenumber": "+79778108745",
        "address": "Красногорск Лесная 5"
    }


def fetch_coordinates():
    apikey = settings.YANDEX_KEY;
    address = "Красногорск Лесная 5"
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    print (lon, lat)
