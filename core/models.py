from django.db import models

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
    

