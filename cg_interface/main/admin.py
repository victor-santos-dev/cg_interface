from django.contrib import admin
from .models import OriginImage, ModifiedImage
# Register your models here.
admin.site.register(OriginImage)
admin.site.register(ModifiedImage)