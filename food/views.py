from .models import Food, Added_Image, FoodOrder
import re, json
from rest_framework.views import APIView
from rest_framework.response import Response
from adrf.views import APIView as ASYNCAPIVIEW

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
        
        search_term = slug.replace("-", " ")
    
        all_foods = Food.objects.filter(name__istartswith=search_term)[:8]
        
        for food in all_foods:
            all_images_container = []
            
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
        
        all_foods = Food.objects.filter(category__iexact=slug)[:12]
        
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
    

class Order(APIView):
    def get(self, request, *args, **kwargs):
        all_orders = FoodOrder.objects.filter(user=request.user)
        
        order_container = []
        
        for order in all_orders:
            order_container.append({
                "name": order.food.name,
                "slug": order.food.slug,
                "price": order.food.price,
                "image": str(order.food.images.all()[0]),
                "amount": order.amount
            })
        
        return Response(order_container)
    
    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        order = FoodOrder()
        
        food = Food.objects.filter(slug=slug).first()
        
        if FoodOrder.objects.filter(food=food).filter(user=request.user).first() is None:
            order.food = food
            
            order.user = request.user
            
            order.amount = request.data.get("amount")
            
            order.save()
            
            return Response({
                'status': 'uploaded'
            })
        else:
            # has already been added 
            
            return Response({
                'status': 'problem here'
            })
            
            
    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        food = Food.objects.get(slug=slug)
        
        order = FoodOrder.objects.filter(food=food).first()
        
        if order is not None:
            order.delete()
            
            return Response({
                'status': 'deleted'
            })
        else:
            # no such order
            
            return Response({
                'status': 'problem here'
            })
            
    def put(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        
        food = Food.objects.get(slug=slug)
        
        order = FoodOrder.objects.filter(food=food).first()
        
        if order is not None:
            order.amount = int(request.data.get("amount"))
            
            order.save()
            
            return Response({
                'status': 'updated'
            })
        else:
            # no such order
            
            return Response({
                'status': 'problem here'
            })
    
    
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
     
     
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class askAIQuestion(ASYNCAPIVIEW):
    async def post(self, request, *args, **kwargs):
        # chat_log = [{"role": "user", "content": "How are you doing?"}]

        chat_log = json.loads(request.data.get("question"))

        client = AsyncOpenAI(
            api_key=os.environ["OPENAIKEY"],  
        )
        
        completion = await client.chat.completions.create(model="gpt-4o-mini", messages=chat_log)

        response = completion.choices[0].message.content
        
        return Response({
            'response': response
        }) 
    
    async def get(self, request, *args, **kwargs):
        return Response({
            'response': "works",
        }) 