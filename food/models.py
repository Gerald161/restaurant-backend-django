from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
class Added_Image(models.Model):
    image = models.ImageField()
    
    def __str__(self):
        return self.image.name
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        
        super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if self.image:
            max_size_kb = 200  # Maximum size in KB

            # Convert KB to bytes
            max_size_bytes = max_size_kb * 1024
            
            if self.image.size > max_size_bytes:
                im = Image.open(self.image)
        
                width, height = im.size
        
                output = BytesIO()
                
                # Calculate the resize factor based on the desired size thresholds
                resize_factor = 1
        
                if self.image.size >= 10 * 1024 * 1024:  # 10 MB
                    resize_factor = 1 / 10
                elif self.image.size >= 5 * 1024 * 1024:  # 5 MB
                    resize_factor = 1 / 7
                elif self.image.size >= 4 * 1024 * 1024:  # 4 MB
                    resize_factor = 1 / 6
                elif self.image.size >= 2 * 1024 * 1024:  # 2 MB
                    resize_factor = 1 / 4
                elif self.image.size >= 1 * 1024 * 1024:  # 1 MB
                    resize_factor = 1 / 3
                else:# 800 KB and below
                    resize_factor = 1 / 2
                    
                new_width = int(width * resize_factor)
                new_height = int(height * resize_factor)

                im = im.resize((new_width, new_height), Image.LANCZOS)
        
                rgb_im = im.convert('RGB')
        
                rgb_im.save(output, format='JPEG', quality=70)
        
                output.seek(0)
        
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0],'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)

class Food(models.Model):
    MEAL_CHOICES = [
        ("breakfast", "Breakfast"), ("lunch", "Lunch"), ("supper", "Supper"), ("drinks", "Drinks")
    ]
    
    name = models.CharField(max_length=300)
    slug = models.SlugField(null=True)
    images = models.ManyToManyField(Added_Image)
    price = models.CharField(max_length=6, default=1)
    category = models.CharField(default="breakfast", choices=MEAL_CHOICES, max_length=20)

    def __str__(self):
        return str(self.slug)

    def delete(self, *args, **kwargs):
        # Delete associated images before deleting the Food model
        for image in self.images.all():
            image.delete()
        
        super().delete(*args, **kwargs)