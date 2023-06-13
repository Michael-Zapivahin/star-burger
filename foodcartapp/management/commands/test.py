
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from foodcartapp.models import Order, OrderItem, Product, RestaurantMenuItem, Restaurant
from django.shortcuts import get_object_or_404, Http404
from rest_framework.serializers import ModelSerializer
from django.urls import reverse
from geodata.models import Place
from django.db.models import F, Q, Count, ObjectDoesNotExist

import foodcartapp.db_operations as db

from geopy import distance

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
                    delivery_distance = get_distance(order.address, restaurants[restaurant].address)
                    order_restaurants.append({
                        'restaurant': restaurants[restaurant],
                        'distance': delivery_distance
                    })

            if order_restaurants:
                order.restaurant_selected = False
                order.restaurant_possible = True
                order.restaurant_distance = order_restaurants[0]['distance']
        else:
            order.restaurant_selected = True



def get_text():
    return {
        "products": [{"product": 3, "quantity": 1}, {"product": 5, "quantity": 2}],
        "firstname": "Michael",
        "lastname": "Zapivahin",
        "phonenumber": "+79778108745",
        "address": "Красногорск Лесная 5"
    }


def fetch_coordinates(apikey, address):
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
    return lon, lat


def get_place_coordinates(api_key, place):

    try:
        place = get_object_or_404(Place, place=place)
        lon, lat = place.lon, place.lat
    except Http404:
        lon, lat = fetch_coordinates(api_key, place)
        Place.objects.create(place=place, lon=lon, lat=lat)

    return lon, lat


def get_distance(place_from, place_to):
    api_key = settings.YANDEX_KEY
    coordinates_from = get_place_coordinates(api_key, place_from)
    # print(place_from, coordinates_from)
    coordinates_to = get_place_coordinates(api_key, place_to)
    # print(place_to, coordinates_to)
    return distance.distance(coordinates_from, coordinates_to).km


def get_orders():
    orders = []
    for order in Order.objects.filter(status__in=['01', '02', '03', '04']).get_order_cost():
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
