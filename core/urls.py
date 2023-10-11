from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/food-items/', FoodItems, name='food-item-api'),
    path('api/add-to-cart/', add_to_cart, name='add-to-cart'),
    path('api/remove-from-cart/', remove_from_cart, name='add-to-cart'),
    path('api/cart-list/', cart_list, name='cart-list'),
    path('api/cart-count/', cart_count, name='cart-count'),


    path('food_items_list/', food_items_list, name='food_items_list'),
    # # path('ajax_datatable/food_items_list/', FoodItemDatatableView.as_view(),
    # #      name="ajax_datatable_food_items_list"),
    path('add_food_items/', add_food_item, name= 'add_food_items'),
    path('food_item_edit/<int:food_item_id>/', food_item_add_edit_view, name='food_item_edit'),
    path('load_content/<str:menu_id>/', load_content, name='load_content'),
    # other URLs
]
