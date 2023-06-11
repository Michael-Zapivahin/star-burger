from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer

import phonenumbers

import foodcartapp.db_operations as db

from .models import Product, Order, OrderItem


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):

    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address', 'products']


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

    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    db.create_order(serializer.validated_data)

    return Response({})


def validate_fields(request_body, field_names):
    if not request_body:
        return Response({
            'response': 'no data',
        }, status=status.HTTP_400_BAD_REQUEST)

    for field_name in field_names:
        try:
            field = request_body[field_name]
        except KeyError:
            return Response({
                'error': f'{field_name} - обязательное поле.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if field_name != 'products' and isinstance(field, list):
            return Response({
                'error': f'В поле {field_name} положили список.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not field:
            return Response({
                'error': f'{field_name} поле не может быть пустым.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if field_name == 'products':
            if not isinstance(field, list):
                return Response({
                    'error': 'products: ожидался list со значениями, но был получен \'str\'.'
                }, status=status.HTTP_400_BAD_REQUEST)

            for product in field:
                if product['product'] > 1000:
                    return Response({
                        'error': f'Недопустимый первичный ключ продукта \'{product["product"]}\''
                    }, status=status.HTTP_400_BAD_REQUEST)

        if field_name == 'phonenumber':
            error_msg = Response({
                'error': 'Введен некорректный номер телефона.'
            }, status=status.HTTP_400_BAD_REQUEST)
            try:
                phonenumber = phonenumbers.parse(field, 'RU')
                if not phonenumbers.is_valid_number(phonenumber):
                    return error_msg
            except phonenumbers.phonenumberutil.NumberParseException:
                return error_msg
