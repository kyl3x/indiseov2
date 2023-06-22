from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from PIL import Image
import requests
from io import BytesIO
import openai
import csv

# Create your views here.

def index(request):
	return render(request,'main/index.html')

def ai(request):
    if request.method == 'POST':
        url = request.POST['url']
        # Call OpenAI API to generate the product description using the URL
        # Replace YOUR_OPENAI_API_KEY with your actual OpenAI API key
        openai.api_key = ''
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f"Generate a product description for the URL: {url}.",
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=None,
            frequency_penalty=0,
            presence_penalty=0
        )
        description = response.choices[0].text.strip()

        return render(request, 'main/ai.html', {'description': description})
    else:
        return render(request, 'main/ai.html')

def image_resize(request):
    if request.method == 'POST':
        try:
            image_url = request.POST.get('image_url')  # Get the image URL from the form input
            width = int(request.POST.get('width'))  # Get the desired width from the form input
            height = int(request.POST.get('height'))  # Get the desired height from the form input
            
            # Download the image from the URL
            response = requests.get(image_url)
            response.raise_for_status()  # Check if the request was successful
            
            # Open the downloaded image
            img = Image.open(BytesIO(response.content))
            
            # Resize the image
            img.thumbnail((width, height))
            
            # Save the resized image
            resized_image_path = 'resized_image.jpg'  # Choose a filename and extension for the resized image
            img.save(resized_image_path, optimize=True, quality=40)
            
            # Serve the resized image for download
            file_response = FileResponse(open(resized_image_path, 'rb'))
            file_response['Content-Disposition'] = 'attachment; filename="resized_image.jpg"'
            return file_response
        
        except (KeyError, requests.exceptions.RequestException, ValueError):
            return HttpResponseServerError("Failed to download and resize the image.")
    
    return render(request, 'main/image-resize.html')

# def inner(request):
#     return render(request,'main/inner-page.html')

def generate_sitemap(file_path):
    # Read the hreflang information from the CSV file
    hreflang_dict = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header row
        for row in reader:
            url = row[0]
            lang = row[1]
            href = row[2]
            if url not in hreflang_dict:
                hreflang_dict[url] = {}
            hreflang_dict[url][lang] = href

    # Generate the XML sitemap
    with open('sitemap.xml', 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n')
        f.write('        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for url, hreflang_dict in hreflang_dict.items():
            f.write('    <url>\n')
            f.write(f'        <loc>{url}</loc>\n')
            for lang, href in hreflang_dict.items():
                f.write(f'        <xhtml:link rel="alternate" hreflang="{lang}" href="{href}" />\n')
            f.write('    </url>\n')
        f.write('</urlset>\n')

def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        file_path = 'media/hreflang.csv'  # Set the desired file path to save the uploaded CSV file
        with open(file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        generate_sitemap(file_path)

        # Serve the generated sitemap CSV file for download
        with open('sitemap.xml', 'r') as f:
            response = HttpResponse(f, content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=sitemap.xml'
            return response
    return render(request, 'main/xml.html')