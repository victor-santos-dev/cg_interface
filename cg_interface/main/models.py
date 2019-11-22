from django.db import models

# Create your models here.
class OriginImage(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.name

class ModifiedImage(models.Model):
    origin = models.ForeignKey(OriginImage,on_delete=models.CASCADE)
    applied_method = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f'{self.origin.name} {self.applied_method}'
     