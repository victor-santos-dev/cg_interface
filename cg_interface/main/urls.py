
from django.urls import path, include
from . import views


urlpatterns = [
    path('index/',views.index , name='index'),
    path('images/<int:pk>/',views.show_image, name='show_image'),
]
