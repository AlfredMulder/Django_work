***************************
Глава 3- приложение Contact
***************************


**Состав и краткое описание**
=============================

Данное приложение отвечает за отправку сообщений с аккаунта на email адрес.
Включает в себя только одно представление(contact) и один шаблон(contact.html)

**Представление contact**
=========================

Листинг::

    def contact(request):
        title = 'Contact'
        form = contactForm(request.POST or None)
        confirm_message = None

        if form.is_valid():
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            subject = 'Message from MYSITE.com'
            message = f'{comment} {name}'
            emailFrom = form.cleaned_data['email']
            emailTo = [settings.EMAIL_HOST_USER]
            #Подключение стандартной django- функции для отправки сообщения на email- адрес.
            send_mail(subject, message, emailFrom, emailTo, fail_silently = True)
            title = "Thanks!"
            confirm_message = "Thanks for message. We will get right back to you."
            form = None

        context = {'title': title, 'form': form, 'confirm_message': confirm_message, }
        template = 'contact.html'
        return render(request, template, context)

**Страница contact:**

.. image:: _static/contact.png
  :target: _static/contact.png
