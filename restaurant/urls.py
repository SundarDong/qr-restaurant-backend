from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.MenuView.as_view(), name='menu'),
    path('table/<str:qr_code>/', views.TableDetailView.as_view(), name='table-detail'),
    path('orders/', views.create_order, name='create-order'),
    path('orders/<uuid:order_id>/', views.order_status, name='order-status'),
    path('orders/<uuid:order_id>/status/', views.update_order_status, name='update-order-status'),
    path('restaurant/orders/', views.restaurant_orders, name='restaurant-orders'),
]