from django import template
from loft.models import Category, Product, FavouriteProduct

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_products(category=None):
    if category:
        return Product.objects.filter(category=category)[::-1]
    return Product.objects.all()[::-1]


@register.simple_tag()
def get_normal_price(price):
    return f"{price:}".replace("_", " ")


@register.simple_tag()
def get_product_colors(color_name):
    products = Product.objects.filter(color_name=color_name)
    colors = [i.color_code for i in products]
    return colors


@register.simple_tag()
def get_favourite_products(user):
    favs = FavouriteProduct.objects.filter(user=user)
    products = [i.product for i in favs]
    return products


@register.simple_tag()
def get_products_by_color(title):
    products = Product.objects.filter(title=title)
    unique_colors = list(set(product.color_code for product in products))
    return unique_colors


@register.simple_tag()
def get_discount_mark(slug):
    try:
        product = Product.objects.get(title=slug)
        return product
    except:
        return None


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()
