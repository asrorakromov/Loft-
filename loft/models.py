from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Категория')
    icon = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Иконка категории')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return '-'

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Продукт')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    quantity = models.IntegerField(default=0, verbose_name='В наличии')
    description = models.TextField(verbose_name='Описание')
    width = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ширина')
    length = models.CharField(max_length=100, blank=True, null=True, verbose_name='Длина')
    high = models.CharField(max_length=100, blank=True, null=True, verbose_name='Высота')
    color_name = models.CharField(max_length=150, verbose_name='Название цвета', default='Белый')
    color_code = models.CharField(max_length=15, verbose_name='Код цвета', default='#ffffff')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип товара')
    discount = models.IntegerField(default=0, verbose_name='Скидка', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)
    model = models.CharField(max_length=300, null=True, blank=True, verbose_name='Модель')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_image_product(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return '-'
        else:
            return '-'

    @property
    def get_discount(self):
        if self.discount:
            discounted_price = self.discount / 100 * self.price
            res = self.price - discounted_price
            return res
        else:
            pass


class Type(models.Model):
    title = models.CharField(max_length=150, verbose_name='Тип товара')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'


class ImageProduct(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Картинка товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'

    def get_image_slider(self):
        if self.image:
            try:
                return self.image.url
            except:
                return '-'
        else:
            return '-'


class FavouriteProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'Клиент: {self.user.username}, Товар: {self.product.title}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Номер телефона')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Email')
    city = models.CharField(max_length=150, verbose_name='Город', blank=True, null=True)
    street = models.CharField(max_length=150, verbose_name='Улица', blank=True, null=True)
    house = models.CharField(max_length=50, verbose_name='Дом/Корпус', blank=True, null=True)
    flat = models.CharField(max_length=50, verbose_name='Квартира', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    first_name = models.CharField(max_length=100, default='', verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=100, default='', verbose_name='Фамилия пользователя')
    email = models.EmailField(max_length=200, blank=True, null=True, verbose_name='Email пользователя')

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    is_completed = models.BooleanField(default=False, verbose_name='Статус заказа')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Покупатель')

    def __str__(self):
        return self.customer.first_name

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_card_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = 0

        for item in order_products:
            product_price = item.product.get_discount if item.product.discount else item.product.price
            total_price += product_price * item.quantity

        return total_price

    @property
    def get_card_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([i.quantity for i in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Продукт')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class Shipping(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Заказ')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    city = models.CharField(max_length=100, verbose_name='Город получателя', blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата доставки')
    first_name = models.CharField(max_length=50, verbose_name='Имя получателя', blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия получателя', blank=True, null=True)
    phone = models.CharField(max_length=50, verbose_name='Номер получателя', blank=True, null=True)

    def __str__(self):
        return f'Доставка по адресу {self.address}  получателю {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Отправитель')
    name = models.CharField(max_length=100, verbose_name='Имя отправителя')
    email = models.EmailField(max_length=200, verbose_name='Email отправителя')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Заявка на связь'
        verbose_name_plural = 'Заявки на связь'


class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    total_price = models.FloatField(default=0, verbose_name='Сумма заказа')

    def __str__(self):
        return f'Покупатель: {self.customer.first_name} {self.customer.last_name}, Номер заказа: {self.pk}'

    class Meta:
        verbose_name = 'История заказа'
        verbose_name_plural = 'Истории заказов'


class SaveOrderProduct(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, verbose_name='Заказ', related_name='products')
    product = models.CharField(max_length=500, verbose_name='Товар')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    product_price = models.FloatField(default=0, verbose_name='Цена товара')
    final_price = models.FloatField(default=0, verbose_name='Общая сумма')
    photo = models.ImageField(upload_to='images/', verbose_name='Фото товара')
    color_name = models.CharField(max_length=50, verbose_name='Цвет')
    state = models.CharField(max_length=50, blank=True, null=True, verbose_name='Статус заказа')
    discount_price = models.FloatField(default=0, blank=True, null=True, verbose_name='Скидочная цена товара')

    def __str__(self):
        return f'Заказ: {self.order}, Продукт: {self.product}'

    class Meta:
        verbose_name = 'История заказанного товара'
        verbose_name_plural = 'История заказанных товаров'


class SaveCard(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Время заказа')
    total_price = models.FloatField(default=0, blank=True, null=True, verbose_name='Итоговая сумма заказа')

    def __str__(self):
        return f'Заказ №{self.id}, покупателя  {self.customer.first_name}'

    class Meta:
        verbose_name = 'Сохраненный заказ'
        verbose_name_plural = 'Сохраненные заказы'


class SaveCardProduct(models.Model):
    save_cart = models.ForeignKey(SaveCard, on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name='Сохраненный заказ')
    product = models.CharField(max_length=255, blank=True, null=True, verbose_name='Заказанный товар')
    quantity = models.IntegerField(default=0, blank=True, null=True, verbose_name='Кол-во')
    product_price = models.FloatField(default=0, blank=True, null=True, verbose_name='Цена товара')
    final_price = models.FloatField(default=0, blank=True, null=True, verbose_name='Итоговая цена товара')
    discount_price = models.FloatField(default=0, blank=True, null=True, verbose_name='Скидочная цена товара')
    product_photo = models.ImageField(upload_to='save_card_product/', blank=True, null=True)
    color_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Цена товара')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Дата')

    state = models.CharField(max_length=150, verbose_name='Статус заказа', blank=True, null=True)

    def __str__(self):
        return f'Заказанный товар {self.product},  покупателя {self.save_card.customer.first_name}'

    class Meta:
        verbose_name = 'Сохраненный заказанный товар'
        verbose_name_plural = 'Сохраненные заказанные товары'


class Card(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def get_card_total_price(self):
        card_products = self.cardproduct_set.all()
        total_price = sum([i.get_total_price for i in card_products])
        return total_price

    @property
    def get_card_total_quantity(self):
        card_products = self.cardproduct_set.all()
        total_quantity = sum([i.quantity for i in card_products])
        return total_quantity

    def __str__(self):
        return f'Корзина №{self.id}, пользователя: {self.customer.first_name}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CardProduct(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='card_products')
    quantity = models.IntegerField(default=0, blank=True, null=True, verbose_name='Количество')

    @property
    def get_total_price(self):
        if self.product.discount:
            return self.product.get_discount * self.quantity
        else:
            return self.product.price * self.quantity

    def __str__(self):
        return f'Товар {self.product.title}. По заказу №{self.card.id}'

    class Meta:
        verbose_name = 'Товар корзины'
        verbose_name_plural = 'Товары корзины'


class RatingProduct(models.Model):
    number = models.IntegerField(default=0, blank=True, null=True, verbose_name='Оценка')
    quantity = models.IntegerField(default=0, blank=True, null=True, verbose_name='Количество оценок')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='rate')

    # def get_rating(self):
    #     if self.quantity > 0 and self.number > 0:
    #         result = self.number / self.quantity
    #         return float(result)
    #     else:
    #         return 0

    def __str__(self):
        return f'Рейтинг {self.product.title}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
