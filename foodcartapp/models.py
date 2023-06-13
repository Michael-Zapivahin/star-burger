from django.db import models
from django.core.validators import MinValueValidator, ValidationError

from phonenumber_field.modelfields import PhoneNumberField


def validate_positive(value):
    if value < 0:
        raise ValidationError(
            f'{value} is not an positive number',
            params={'value': value},
        )


class OrderQuerySet(models.QuerySet):
    def get_order_cost(self):
        orders = self.annotate(cost=models.Sum(
            models.F('products__quantity') * models.F('products__product__price')
        ))
        return orders


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    CASH = 'CASH'
    CARD = 'CARD'
    PAYMENT_TYPE = [
        (CASH, 'Наличными'),
        (CARD, 'Картой'),
    ]
    payment = models.CharField(
        'Способ оплаты',
        choices=PAYMENT_TYPE,
        max_length=15,
        db_index=True,
        default=CASH
    )
    NEW = '01'
    COOKING = '02'
    DELIVERY = '03'
    DONE = '04'
    ORDER_STATUS = [
        (NEW, 'Не обработан'),
        (COOKING, 'Готовится'),
        (DELIVERY, 'Доставка'),
        (DONE, 'Доставлен'),
    ]
    status = models.CharField(
        'Статус',
        choices=ORDER_STATUS,
        default=NEW,
        max_length=15,
        db_index=True
    )
    firstname = models.CharField(
        'Имя',
        max_length=50
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=100,
        blank=True,
    )

    phonenumber = PhoneNumberField(verbose_name='телефон', db_index=True)

    address = models.CharField('адрес доставки', max_length=100, blank=True)

    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    registration_date = models.DateTimeField(
        blank=True, null=True, verbose_name='Дата регистрации', db_index=True, auto_now=True
    )

    call_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата звонка', db_index=True)

    delivery_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата доставки', db_index=True)

    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Ресторан',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.firstname} {self.phonenumber}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='products',
        verbose_name="заказы",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='product_items',
        verbose_name="продукты",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField('Количество')

    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена', validators=[validate_positive])

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        unique_together = [
            ['order', 'product']
        ]

    def __str__(self):
        return f"{self.order.phonenumber} - {self.product.name}"


