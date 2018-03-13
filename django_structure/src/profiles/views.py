from django.shortcuts import render

# Create your views here.
#Подключение функций для работы страниц: home, about.
def home(request):
    context = locals()
    template = 'home.html'
    return render(request, template, context)

def about(request):
    context = locals()
    template = 'about.html'
    return render(request, template, context)
