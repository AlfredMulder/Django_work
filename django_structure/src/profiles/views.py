from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
#Подключение функций для работы страниц: home, about, userProfile.
def home(request):
    context = {}
    template = 'home.html'
    return render(request, template, context)

def about(request):
    context = {}
    template = 'about.html'
    return render(request, template, context)

#Декоратор, требующий обязательного входа в профиль.
@login_required
def userProfile(request):
    user = request.user
    context = {'user': user}
    template = 'profile.html'
    return render(request, template, context)
