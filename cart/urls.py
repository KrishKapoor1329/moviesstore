from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add, name='cart.add'),
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('cart/<int:cart_id>/clear/', views.clear_cart, name='cart.clear_cart'),
    path('cart/<int:cart_id>/item/<int:item_id>/remove/', views.remove_item, name='cart.remove_item'),
    path('cart/<int:cart_id>/checkout/', views.checkout, name='cart.checkout'),
]
