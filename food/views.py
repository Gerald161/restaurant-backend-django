from django.http import JsonResponse, HttpResponse
from .models import Food, Added_Image
import re, json
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Upload(APIView):
    def post(self, request, *args, **kwargs):
        food = Food()
        
        food.name = request.data.get("name")
        
        food.price = request.data.get("price")
        
        food.category = request.data.get("category")
        
        food.save()
        
        slug = re.sub(r'\s', "-", request.POST.get('name').lower())
        
        food.slug = slug
        
        food.slug = f"{food.slug}-{food.id}"

        food.save()
        
        for image in request.FILES.values():
            added_image = Added_Image()
            
            added_image.image = image
            
            added_image.save()
            
            food.images.add(added_image)
    
        return Response({
            'status': 'complete'
        })
        

class Remove(APIView):
    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        try:
            food = Food.objects.filter(slug=slug).first()
            
            # if food is not None alternatively
            
            food.delete()
            
            return Response({
                'status': 'deleted'
            })
        except:
            return Response({
                'status': 'not found'
            })
            

class Search(APIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        food_json_container = []
            
        all_images_container = []
        
        if request.POST.get('search') is not None:
            search_term = request.POST.get('search').lower()
            
            all_foods = Food.objects.filter(name__istartswith=search_term)[:8]
            
            for food in all_foods:    
                food_json_container.append({
                    "name": food.name,
                })
            
            return Response(food_json_container)
        else:
            search_term = slug.replace("-", " ")
        
            all_foods = Food.objects.filter(name__istartswith=search_term)[:8]
            
            for food in all_foods:
                for image in food.images.all():
                    all_images_container.append(str(image))
                
                food_json_container.append({
                    "name": food.name,
                    "slug": food.slug,
                    "price": food.price,
                    "category": food.category,
                    "images": all_images_container
                })
            
            return Response(food_json_container)
    

class Category(APIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        category = slug.replace("-", " ")
        
        all_foods = Food.objects.filter(category__iexact=category)[:12]
        
        food_json_container = []
        
        for food in all_foods:
            image = str(food.images.all()[0])
            
            food_json_container.append({
                "name": food.name,
                "slug": food.slug,
                "price": food.price,
                "image": image
            })
        
        return Response(food_json_container)
    
    
class Dish_Details(APIView):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        try:
            all_images_container = []
            
            food = Food.objects.filter(slug=slug).first()
            
            for image in food.images.all():
                all_images_container.append(str(image))
            
            return Response({
                "name": food.name,
                "slug": food.slug,
                "price": food.price,
                "category": food.category,
                "images": all_images_container
            })
        except:
            return Response({
                'status': 'not found'
            })
            
    def put(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        food = Food.objects.get(slug=slug)
        
        food.name = request.data.get("name")
        
        food.price = request.data.get("price")
        
        food.category = request.data.get("category")
        
        indicesToRemove = json.loads(request.data.get("image_index_to_remove"))
        
        if len(indicesToRemove) > 0:
            for index in indicesToRemove:
                food.images.all()[index].delete()
        
        for image in request.FILES.values():
            added_image = Added_Image()
            
            added_image.image = image
            
            added_image.save()
            
            food.images.add(added_image)
        
        food.save()
        
        return Response({
            'status': 'updated'
        })