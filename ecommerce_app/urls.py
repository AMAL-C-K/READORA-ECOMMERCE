from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('<slug:slug>',views.genrewise_list,name='genre'),
    path('<slug:g_slug>/<slug:b_slug>',views.book, name='book'),
    path('search/',views.search, name='search'),
    path('price-filter/',views.price_filter, name='price-filter')

]