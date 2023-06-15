from django import forms
from django.shortcuts import redirect, render, get_object_or_404, Http404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.urls import reverse

import requests
from geopy import distance

import star_burger.settings as settings

from foodcartapp.models import Product, Restaurant, Order, RestaurantMenuItem
from geodata.models import Place


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    orders = list(Order.objects.exclude(status=Order.DONE).get_order_cost().order_by('status'))
    menu_items = RestaurantMenuItem.objects.filter(availability=True).values('restaurant', 'product')
    restaurants = {}
    for item in menu_items:
        restaurants[f'restaurant_{item["restaurant"]}'] = get_object_or_404(Restaurant, pk=item["restaurant"])
    for order in orders:
        order.id_admin_url = reverse('admin:foodcartapp_order_change', args=(order.id,))
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

            its_one = True
            for _, restaurant in enumerate(order_restaurants):
                if its_one or (restaurant['distance'] < delivery_distance):
                    delivery_distance = restaurant['distance']
                    order.restaurant_selected = False
                    order.restaurant_possible = f'{restaurant["restaurant"].name}, {round(delivery_distance, 0)} км.'
                    its_one = False
        else:
            order.restaurant_selected = True

    return render(request, template_name='order_items.html', context={
        'order_items': orders
    })


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    try:
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    except requests.exceptions.RequestException:
        return None

    if found_places:
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
    coordinates_to = get_place_coordinates(api_key, place_to)
    return distance.distance(coordinates_from, coordinates_to).km
