from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

import foodcartapp.db_operations as db

from .models import Product



import json


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    # db.create_order(request.data)
    # order_content = request.data
    # products = []
    # try:
    #     for product_key in order_content['products']:
    #         product = {
    #             'pk': int(product_key['product']),
    #             'quantity': product_key['quantity'],
    #         }
    #         products.append(product)
    #     if not order_content['products']:
    #         products.append({'error loop ': order_content['products']})
    # except KeyError or TypeError as error:
    #     products.append({'error products ': str(error)})
    # except:
    #     products.append({'error products ': 'none'})
    try:
        products = request.data['products']
        if not products:
            return Response({'products': 'Это поле не может быть пустым.'})
    except KeyError:
        return Response({'products': 'Обязательное поле.'})
    if not isinstance(products, list) or len(products):
        return Response({'products': 'Ожидался list со значениями, но был получен "str".'})
    else:
        order = request.data
        print(order)

    # TODO это лишь заглушка
    return Response(products)

