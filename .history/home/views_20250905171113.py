from django.shortcuts import render
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html')
def about(request):
    return render(request, 'home/about.html')
# Create your views here.
