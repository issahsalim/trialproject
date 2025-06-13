from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils.text import slugify
import requests

# Create your models here.



class  USERACCOUNT(AbstractUser):
    Course=models.CharField(max_length=255) 
    

#      question 
class Questions(models.Model):
    question1= models.CharField(max_length=255)
    question1= models.CharField(max_length=255)
    question2= models.CharField(max_length=255)
    question3= models.CharField(max_length=255)
    question4= models.CharField(max_length=255)
    question5= models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question1[:7]}......"


from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True)  # Add this field
    latitude = models.FloatField(null=True, blank=True) 
    longitude = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='places/')
    description = models.TextField()
    category = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.address:
            # First try to geocode from name if address is empty
            geocode_query = self.address if self.address else self.name
            response = requests.get(
                f'https://maps.googleapis.com/maps/api/geocode/json?address={geocode_query}&key=AIzaSyCafX1QPC_yhAnBuffdjSilnybuGlpgPcM'
            ) 
            data = response.json()  
            if data['results']: 
                result = data['results'][0]
                self.latitude = result['geometry']['location']['lat']
                self.longitude = result['geometry']['location']['lng']
                if not self.address:
                    self.address = result['formatted_address']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SupportMember(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='support_members/')
    contact_number = models.CharField(max_length=15)
    role = models.CharField(max_length=100, blank=True)  # e.g., "Tech Support", "Security"

    def __str__(self):
        return self.name
    

    


# class Place(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6)
#     image = models.ImageField(upload_to='places/')
#     slug = models.SlugField(unique=True, blank=True)
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)
    
#     def __str__(self):
#         return self.name


