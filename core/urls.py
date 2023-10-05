from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/food-items/', FoodItemAPIView.as_view(), name='food-item-api'),
    path('food_items_list/', food_items_list, name='food_items_list'),
    # # path('ajax_datatable/food_items_list/', FoodItemDatatableView.as_view(),
    # #      name="ajax_datatable_food_items_list"),
    path('add_food_items/', food_item_add_edit_view, name= 'add_food_items'),
    path('food_item_edit/<int:food_item_id>/', food_item_add_edit_view, name='food_item_edit'),
    path('load_content/<str:menu_id>/', load_content, name='load_content'),
    # other URLs
]
