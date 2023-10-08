from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(FoodItem)
admin.site.register(ShoppingCart)
# admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Days)
admin.site.register(TodaysSpecial)



