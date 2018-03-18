from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
#Приложение для проверки наличия пользователя в сети
@login_required
def checkout(request):
    context = {}
    template = 'checkout.html'
    return render(request, template, context)
