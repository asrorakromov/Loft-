from .models import Product, OrderProduct, Customer, Order


class CardForAuthenticatedUser:
    def __init__(self, request, product_id=None, action=None, quantity=1):
        self.user = request.user
        self.quantity = quantity
        if product_id and action:
            self.add_or_delete(product_id, action)

    def get_card_info(self):
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.orderproduct_set.all()

        card_total_quantity = order.get_card_total_quantity
        card_total_price = order.get_card_total_price
        product_count = order_products.count()

        return {
            'card_total_quantity': card_total_quantity,
            'card_total_price': card_total_price,
            'order': order,
            'products': order_products,
            'product_count': product_count
        }

    def add_or_delete(self, product_id, action):
        order = self.get_card_info()['order']
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity >= self.quantity:
            order_product.quantity += self.quantity
            product.quantity -= self.quantity
        elif action == 'delete':
            order_product.quantity -= self.quantity
            product.quantity += self.quantity

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear_basket(self):
        order = self.get_card_info()['order']
        order_products = order.orderproduct_set.all()
        for product in order_products:
            product.delete()
        order.save()


def get_card_data(request):
    card = CardForAuthenticatedUser(request)
    card_info = card.get_card_info()
    return {
        'card_total_quantity': card_info['card_total_quantity'],
        'card_total_price': card_info['card_total_price'],
        'order': card_info['order'],
        'products': card_info['products'],
        'product_count': card_info['product_count'],
    }
