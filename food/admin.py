from django.contrib import admin
from .models import Food, Added_Image, FoodOrder

# Register your models here.
admin.site.register(Food)
admin.site.register(Added_Image)
admin.site.register(FoodOrder)