from django.shortcuts import render
from .forms import UploadImageForm, MethodForm
from .models import OriginImage, ModifiedImage
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
###############
import cv2 as cv
import matplotlib.pyplot as plt
from scipy import misc,ndimage
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
import pytesseract
import sys
import string
import re, os
from io import BytesIO

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UploadImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()

    images = OriginImage.objects.all()
    form = UploadImageForm()
    return render(request,'main/index.html', {'form':form, 'images': images})

def show_image(request, pk):
    methods = {
        'black white': blackwhite,
        'histogram': histogram,
        'gray pattern': grayPattern,
        'laplace filter':laplaceFilter,
        'filter one': filter_one,
    }

    image = OriginImage.objects.get(pk=pk)
    if request.method == 'POST':
        form = MethodForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data['method_name']
            modified_image = methods[method](image)        
            modified_image_model = ModifiedImage(origin=image,applied_method=method,image=modified_image)
            modified_image_model.save()
        

    related_images = ModifiedImage.objects.filter(origin=image)
    form = MethodForm()
    return render(request,'main/show_image.html', {'origin_image':image,'related_images':related_images, 'form':form})
    
    

def blackwhite(image):
    modified_image = Image.open(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/media/{image.image}')
    modified_image = modified_image.convert('L')
    modified_image = modified_image.convert('1')
    image_io = BytesIO()
    modified_image.save(image_io, format='JPEG', quality=100)
    img_content = ContentFile(image_io.getvalue(), 'img.jpg')
    return img_content

def histogram(image):
    image_io = BytesIO()
    a = cv.imread(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/media/{image.image}')
    hist = cv.calcHist([a], [0], None, [256], [0, 256])
    hist, bins = np.histogram(a.ravel(), 256, [0, 256])
    plt.hist(a.ravel(), 256, [0, 256])
    plt.savefig(image_io, format="JPEG")
    img_content = ContentFile(image_io.getvalue(), 'img.jpg')
    return img_content

def grayPattern(image):
    image_io = BytesIO()
    img = cv.imread(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/media/{image.image}')
    img_gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    img_gray = Image.fromarray(img_gray)
    img_gray.save(image_io, format='JPEG')
    img_content = ContentFile(image_io.getvalue(), 'img.jpg')
    return img_content

def laplaceFilter(image):
    image_io = BytesIO()
    img = cv.imread(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/media/{image.image}')
    lap = cv.Laplacian(img, cv.CV_64F)
    lap = np.uint8(np.absolute(lap))
    img_lap = np.vstack([img, lap])
    img_lap = Image.fromarray(img_lap)
    img_lap.save(image_io, format='JPEG')
    img_content = ContentFile(image_io.getvalue(), 'img.jpg')
    return img_content



def filter_one(image):
    image_io = BytesIO()
    img2 = cv.imread(f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/media/{image.image}')
    img = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    (T, Thresh1) = cv.threshold(img, 44, 54, cv.THRESH_TRUNC)
    (T, Thresh3) = cv.threshold(Thresh1, 43, 44, cv.THRESH_BINARY)
    (T,Thresh2) = cv.threshold(Thresh3, 0, 255,cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    (T, Thresh4) = cv.threshold(Thresh2, 30, 255, cv.CALIB_CB_ADAPTIVE_THRESH)
    img_result = Image.fromarray(Thresh4)
    img_content = ContentFile(image_io.getvalue(), 'img.jpg')
    return img_content