from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .utils import CardForAuthenticatedUser, get_card_data
from .forms import LoginForm, RegistrationForm, CreateProfileForm, CustomerForm, ShippingForm, ChangeAccountForm, \
    ChangeProfileForm
from .models import Category, Product, FavouriteProduct, Customer, Contact, SaveOrder, SaveOrderProduct, SaveCard, \
    RatingProduct,Shipping
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
import stripe
from onlineStore import settings
from django.db.models import Q


class ProductList(ListView):
    model = Product
    context_object_name = 'categories'
    template_name = 'loft/index.html'
    extra_context = {
        'title': 'Loft Мебель'
    }

    def get_queryset(self):
        categories = Category.objects.filter(parent=None)
        return categories


class CategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'loft/category_page.html'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category).order_by('-id')
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        categories = Category.objects.all()
        products = Product.objects.filter(category=category)

        if category.slug == 'akciya':
            discounts = Product.objects.all()
            products = [i for i in discounts if i.discount]

        context['title'] = category.title
        context['categories'] = categories
        context['products'] = products[::-1]
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.all()[::-1]
        ratings = RatingProduct.objects.filter(product=product)
        if ratings:
            final_rating = sum([i.number for i in ratings])
            final_num = sum([i.quantity for i in ratings])
            result = final_rating / final_num
            context['result'] = result

        nums = range(product.quantity + 1)

        try:
            status = RatingProduct.objects.get(product=product, user=self.request.user)
            context['status'] = status
        except:
            print('no rating --------------------------------------------------')

        context['sizes'] = [
            {'length': product.length, 'width': product.width, 'height': product.high},
        ]
        context['quantities'] = range(1, product.quantity + 1)
        context['title'] = f'{product.category}: {product.title}'
        context['products'] = products
        context['nums'] = nums
        return context


class FavouritesView(ListView):
    model = FavouriteProduct
    context_object_name = 'favourite_products'
    template_name = 'loft/favourite.html'

    def get_queryset(self):
        user = self.request.user
        products = FavouriteProduct.objects.filter(user=user)
        return [favourite.product for favourite in products]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = 'Избранное'
        return context


def save_favourite_product(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = request.user
        product = Product.objects.get(slug=slug)

        favourite, created = FavouriteProduct.objects.get_or_create(user=user, product=product)
        if created:
            pass
        else:
            favourite.delete()
        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)


def registration(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            register_form = RegistrationForm(request.POST)
            profile_form = CreateProfileForm(request.POST)

            if register_form.is_valid() and profile_form.is_valid():
                user = register_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect('login')

        else:
            register_form = RegistrationForm()
            profile_form = CreateProfileForm()

        context = {
            'register_form': register_form,
            'profile_form': profile_form,
            'categories': categories
        }
        return render(request, 'loft/login.html', context)


def login_user(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            login_form = LoginForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')
        else:
            login_form = LoginForm()

        context = {
            'login_form': login_form,
            'categories': categories
        }
        return render(request, 'loft/login.html', context)


def logout_user(request):
    if not request.user.is_authenticated:
        return redirect('main')
    else:
        logout(request)
        return redirect('main')


def to_card(request, product_id, action):
    if request.user.is_authenticated:
        # Retrieve the quantity from GET parameters; default to 1 if not specified
        quantity = int(request.GET.get('quantity', 1))

        # Pass the quantity to CardForAuthenticatedUser
        user_card = CardForAuthenticatedUser(request, product_id, action, quantity=quantity)

        next_page = request.META.get('HTTP_REFERER', 'main')
        return redirect(next_page)
    else:
        return redirect('register')


def card_view(request):
    if request.user.is_authenticated:
        card_info = get_card_data(request)
        user_card = CardForAuthenticatedUser(request).get_card_info()

        context = {
            'card_total_quantity': card_info['card_total_quantity'],
            'card_total_price': card_info['card_total_price'],
            'order': card_info['order'],
            'products': card_info['products'],
            'product_count': card_info['product_count'],
            'title': 'Корзина'
        }
        return render(request, 'loft/basket.html', context)
    else:
        return redirect('register')


def checkout(request):
    if request.user.is_authenticated:
        card_info = get_card_data(request)

        context = {
            'card_total_quantity': card_info['card_total_quantity'],
            'order': card_info['order'],
            'items': card_info['products'],
            'customer_form': CustomerForm(),
            'shipping_form': ShippingForm(),
            'title': 'Оформление заказа'
        }

        return render(request, 'loft/checkout.html', context)


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        user_card = CardForAuthenticatedUser(request)
        card_info = user_card.get_card_info()

        customer_form = CustomerForm(data=request.POST)
        if customer_form.is_valid():
            customer = Customer.objects.get(user=request.user)
            customer.first_name = customer_form.cleaned_data['first_name']
            customer.last_name = customer_form.cleaned_data['last_name']
            customer.email = customer_form.cleaned_data['email']
            customer.save()

        shipping_form = ShippingForm(data=request.POST)
        if shipping_form.is_valid():
            if user_card.get_card_info()['order'].pk not in [i.order_id for i in Shipping.objects.all()]:
                address = shipping_form.save(commit=False)
                address.customer = Customer.objects.get(user=request.user)
                address.order = user_card.get_card_info()['order']
                address.save()
        else:
            for field in shipping_form.errors:
                print(
                    f"Shipping form errors: {shipping_form.errors} -------")

        total_price = card_info['card_total_price']
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': 'Товары с LoftМебель'
                    },
                    'unit_amount': int(total_price) * 100
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('checkout'))
        )
        return redirect(session.url, 303)


def product_by_color_view(request, title, color):
    product = get_object_or_404(Product, title=title, color_code=color)
    nums = range(product.quantity + 1)

    context = {
        'product': product,
        'nums': nums,
        'color': product.color_code,
        'title': f'{product.category}: {product.title}'
    }
    return render(request, 'loft/product_detail.html', context)


def about_view(request):
    categories = Category.objects.all()
    context = {
        'title': 'О нас',
        'categories': categories
    }
    return render(request, 'loft/about.html', context)


def contact_view(request):
    categories = Category.objects.all()
    context = {
        'title': 'Контакты',
        'categories': categories
    }

    if not request.user.is_authenticated:
        return redirect('register')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(
            user=request.user,
            name=name,
            email=email,
            message=message
        )

    return render(request, 'loft/contact.html', context)


def success_payment(request):
    if request.user.is_authenticated:
        user_card = CardForAuthenticatedUser(request)
        categories = Category.objects.all()
        card_info = user_card.get_card_info()
        order = card_info['order']
        order_save = SaveOrder.objects.create(customer=order.customer, total_price=order.get_card_total_price)
        order_save.save()
        order_products = order.orderproduct_set.all()
        for product in order_products:
            save_order_product = SaveOrderProduct.objects.create(order_id=order_save.pk,
                                                                 product=str(product),
                                                                 quantity=product.quantity,
                                                                 product_price=product.product.price,
                                                                 final_price=product.get_total_price,
                                                                 photo=product.product.get_image_product(),
                                                                 color_name=product.product.color_name)
            save_order_product.save()

        user_card.clear_basket()
        context = {
            'title': 'Оплата прошла успешно',
            'categories': categories
        }

        return render(request, 'loft/success.html', context)
    else:
        return redirect('main')


def edit_account_and_profile_view(request):
    categories = Category.objects.all()
    if not request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        acc_form = ChangeAccountForm(request.POST, instance=request.user)
        profile_form = ChangeProfileForm(request.POST, instance=request.user.profile)

        if acc_form.is_valid() and profile_form.is_valid():
            acc_form.save()
            profile_form.save()
        else:
            return redirect('profile')
    else:
        acc_form = ChangeAccountForm(instance=request.user)
        profile_form = ChangeProfileForm(instance=request.user.profile)

    try:
        customer = Customer.objects.get(user=request.user)

        save_orders = SaveOrder.objects.filter(customer=customer).order_by('-created_at')

        save_carts = [order.products.all() for order in save_orders]

    except Customer.DoesNotExist:
        save_carts = None
        print('Нет продуктов')

    context = {
        'acc_form': acc_form,
        'profile_form': profile_form,
        'save_carts': save_carts,
        'categories': categories,
        'title': 'Профиль'
    }

    return render(request, 'loft/profile.html', context)


def search(request):
    if request.method == 'POST':
        text = request.POST.get('search', '').strip()

        if text:
            products = Product.objects.filter(
                Q(title__icontains=text) | Q(category__title__icontains=text)
            )
        else:
            products = Product.objects.none()

        context = {
            'products': products,
            'title': 'Результаты поиска'
        }

        return render(request, 'loft/category_page.html', context)
    else:
        return redirect('main')


def rating_view(request, slug):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            number = request.POST.get('rating')
            product = Product.objects.filter(slug=slug)
            rating, created = RatingProduct.objects.update_or_create(product=product, user=request.user)

            if created:
                rating.number += int(number)
                rating.quantity += 1
            else:
                rating.number = int(number)
                rating.quantity = 1

            rating.save()

            return redirect('product', slug)

        else:
            return redirect('product', slug)

