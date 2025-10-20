from django.shortcuts import render

# Create your views here.
def no_access_pages(request):
    return render(request,'no_access_page.html')