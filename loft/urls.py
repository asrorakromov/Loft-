from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='main'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('favourite/', FavouritesView.as_view(), name='favourite'),
    path('save_favourite/<slug:slug>/', save_favourite_product, name='save_favourite'),
    path('register/', registration, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('to_card/<int:product_id>/<str:action>/', to_card, name='to_card'),
    path('basket/', card_view, name='basket'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', create_checkout_session, name='payment'),
    path('product_color/<str:title>/<str:color>/', product_by_color_view, name='color'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('success/', success_payment, name='success'),
    path('profile/', edit_account_and_profile_view, name='profile'),
    path('search/', search, name='search'),
    path('rating/<slug:slug>/rating', rating_view, name='rating'),


]
