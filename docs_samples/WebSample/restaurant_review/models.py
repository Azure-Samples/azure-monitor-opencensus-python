from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.CharField(max_length=500)
    review_date = models.DateTimeField('review date')    
    image_name = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.restaurant.name + " (" + self.review_date.strftime("%x") +")"
