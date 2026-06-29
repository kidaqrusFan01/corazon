from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # AUTH ROUTES - this makes login/logout work
    path('accounts/', include('django.contrib.auth.urls')),


    path(
    'add-product/',
    views.add_product,
    name='add_product'
),
   

    path(
    'wishlist/add/<int:product_id>/',
    views.add_to_wishlist,
    name='add_to_wishlist'
),

    path(
    'search/',
    views.search_products,
    name='search_products'
),

    path(
    'category/<slug:slug>/',
    views.category_products,
    name='category'
),

    path(
    'ajax/add/<int:product_id>/',
    views.ajax_add_to_cart,
    name='ajax_add_to_cart'
),

    path(
    'remove/<int:product_id>/',
    views.remove_item,
    name='remove_item'
),


    path(
        'cart/',
        views.cart_view,
        name='cart'
    ),


    path('signup/', views.signup_view, name='signup'), 




    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'increase/<int:product_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease/<int:product_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'product/<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),
    path(
    'dashboard/',
    views.dashboard,
    name='dashboard'

    
),


]