from django.contrib import admin
from django.utils.safestring import mark_safe
from .forms import CategoryForm

from .models import *

# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(ImageProduct)
admin.site.register(Type)
admin.site.register(Profile)
admin.site.register(Customer)
admin.site.register(OrderProduct)
admin.site.register(Contact)
admin.site.register(Shipping)
admin.site.register(SaveOrder)
admin.site.register(SaveOrderProduct)
admin.site.register(RatingProduct)


class ImageProductInline(admin.TabularInline):
    fk_name = 'product'
    model = ImageProduct
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_category_icon')
    prepopulated_fields = {'slug': ('title',)}
    form = CategoryForm

    def get_category_icon(self, obj):
        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" width="50px">')
        else:
            return 'Нет иконки'

    get_category_icon.short_description = 'Фото'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'type', 'model', 'width', 'length', 'high', 'quantity', 'price',
                    'discount', 'created_at', 'get_product_image')
    list_display_links = ('id', 'title')
    list_editable = ('category', 'quantity', 'price', 'model')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'quantity', 'price', 'discount', 'created_at')
    inlines = [ImageProductInline]

    def get_product_image(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="70px">')
            except:
                return '-'
        else:
            return 'Нет фотографии'

    get_product_image.short_description = 'Фото'


@admin.register(FavouriteProduct)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


class OrderProductTabular(admin.TabularInline):
    fk_name = 'order'
    model = OrderProduct


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'get_card_total_quantity', 'get_card_total_price', 'created_at')
    list_display_links = ('pk', 'customer')
    inlines = [OrderProductTabular]
