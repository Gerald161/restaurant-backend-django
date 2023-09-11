from django.http import JsonResponse, HttpResponse
from .models import Food, Added_Image
import re
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Upload(APIView):
    def post(self, request, *args, **kwargs):
        food = Food()
        
        food.name = request.data.get("name")
        
        food.price = request.data.get("price")
        
        food.slug = re.sub(r'\s', "-", request.POST.get('name').lower())
        
        food.save()
        
        for image in request.FILES.values():
            added_image = Added_Image()
            
            added_image.image = image
            
            added_image.save()
            
            food.images.add(added_image)
    
        return Response({
            'status': 'complete'
        })