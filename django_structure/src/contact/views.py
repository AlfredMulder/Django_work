from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import contactForm
# Create your views here.
def contact(request):
    form = contactForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = 'Message from MYSITE.com'
        message = '{0} {1}'.format(comment, name)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.email_host_user]
        #Подключение стандартной django- функции для отправки сообщения на email- адрес.
        send_mail(name, comment, subject, message, emailFrom, emailTo, fail_silently=True)
    context = locals()
    template = 'contact.html'
    return render(request, template, context)
