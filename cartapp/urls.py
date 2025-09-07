from django.urls import path
from . import views
urlpatterns = [
    path('my-cart/',views.cart, name='cart'),
    path('add/<int:book_id>',views.add_to_cart,name='add'),
    path('quantity_plus/<int:cart_id>', views.quantity_plus,name='plus'),
    path('quantity_minus/<int:cart_id>',views.quantity_minus, name='minus'),
    path('remove/<int:cart_id>',views.remove, name='remove'),

    path('checkout/<int:cart_id>', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('orders/',views.orders, name='orders')
]