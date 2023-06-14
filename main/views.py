from django.shortcuts import render
from PIL import Image
import requests
from io import BytesIO

# Create your views here.

def index(request):
	return render(request,'main/index.html')

def upload(request):
    if request.method == 'POST':
        # Retrieve the uploaded image from the form
        uploaded_file = request.FILES['image']
        
        # Download the image from the URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Resize the image
        img = Image.open(image_path)
        img.thumbnail((600, 600))
        
        # Save the resized image
        resized_image_path = 'resized_image.jpg'  # Choose a filename and extension for the resized image
        img.save(resized_image_path, optimize=True, quality=40)
        
        # Pass the paths of the original and resized images to the template
        context = {
            'original_image_path': image_path,
            'resized_image_path': resized_image_path,
        }
        return render(request, 'main/result.html', context)

    return render(request, 'main/upload.html')

def inner(request):
    return render(request,'main/inner-page.html')