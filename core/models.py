from django.db import models
import uuid
# Create your models here.
def upload_to(instance, filename):
    return f'media/{filename}'

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='food_images/',blank= True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Days(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class TodaysSpecial(models.Model):
    food = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    day = models.OneToOneField(Days, on_delete=models.CASCADE)

    def __str__(self):
        return f'Today\'s Special for {self.day}: {self.food.name}'
    
import uuid
# from django.db import models

class ShoppingCart(models.Model):
    shopping_cart_id = models.UUIDField(default=uuid.uuid4, editable=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    ip_location = models.CharField("Ip Location", max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=17, decimal_places=2, null=True, blank=True)
    number_of_items = models.PositiveIntegerField(default=0)
    is_current = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calculate total price and number of items based on CartItems
        self.total_price = sum(item.food_item.price * item.quantity for item in self.cartitem_set.all())
        self.number_of_items = sum(item.quantity for item in self.cartitem_set.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.shopping_cart_id)


class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_cost(self):
        return self.quantity * self.food_item.price

    def __str__(self):
        return f'{self.quantity} x {self.food_item.name} in cart'

