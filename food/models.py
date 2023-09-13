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
            if self.image.size > 35000:
                im = Image.open(self.image)
        
                width, height = im.size
        
                output = BytesIO()
        
                if self.image.size >= 10000000:
                    im = im.resize((width // 20, height // 20), Image.Resampling.LANCZOS)
                elif self.image.size >= 5000000:
                    im = im.resize((width // 10, height // 10), Image.Resampling.LANCZOS)
                elif self.image.size >= 4000000:
                    im = im.resize((width // 6, height // 6), Image.Resampling.LANCZOS)
                elif self.image.size >= 2000000:
                    im = im.resize((width // 4, height // 4), Image.Resampling.LANCZOS)
                elif self.image.size >= 1000000:
                    im = im.resize((width // 3, height // 3), Image.Resampling.LANCZOS)
                elif self.image.size >= 800000:
                    im = im.resize((width // 2, height // 2), Image.Resampling.LANCZOS)
                elif self.image.size >= 500000:
                    im = im.resize((width // 5, height // 5), Image.Resampling.LANCZOS)
                elif self.image.size >= 300000:
                    im = im.resize((width // 4, height // 4), Image.Resampling.LANCZOS)
                elif self.image.size >= 150000:
                    im = im.resize((width // 3, height // 3), Image.Resampling.LANCZOS)
                elif self.image.size >= 100000:
                    im = im.resize((width // 2, height // 2), Image.Resampling.LANCZOS)
                else:
                    im = im.resize((width // 2, height // 2), Image.Resampling.LANCZOS)
        
                rgb_im = im.convert('RGB')
        
                rgb_im.save(output, format='JPEG', quality=70)
        
                output.seek(0)
        
                self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0],'image/jpeg', sys.getsizeof(output), None)

        super().save(*args, **kwargs)

class Food(models.Model):
    MEAL_CHOICES = [
        ("breakfast", "Breakfast"), ("lunch", "Lunch"), ("supper", "Supper")
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