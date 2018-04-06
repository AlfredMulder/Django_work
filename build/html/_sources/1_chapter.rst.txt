***************************
Глава 1- приложение Profile
***************************


**Состав и краткое описание**
=============================

Данное приложение служит двум вещам:

* Объявление полей профиля пользователя для редактирование и обновление оных через "админку".
* Генерации уникального идентификатора службы Stripe.

Состоит из следующих моделей(классов моделей):

#. Profile
#. userStripe

Имеет следующие представления(классы представлений):

#. Home
#. About
#. userProfile

Включает в себя следующие шаблоны:

#. about.html - страница с описанием приложения.
#. base.html - шаблон- основа для всех остальных страниц.
#. footer.html - элемент страницы для указания года выпуска приложения, организации производителя и т.д..
#. home.html - домашняя страница приложения.
#. navbar.html - навигационная панель.
#. profile.html - страница профиля пользователя.

Разберем каждый класс отдельно.

**Класс Profile**
=================


Состоит из следующих полей: name, description, job, street, city, state, phone, website, image, last name, email, user.

Имеет только один метод: __unicode__, возвращающий имя пользователя в юникоде.

Данные поля заполняются пользователями- администраторами приложения.

Листинг::

    class Profile(models.Model):
        name = models.CharField(max_length=120)
        description = models.TextField(default='description default text')
        job = models.CharField(max_length=120, null=True, default='')
        street = models.CharField(default='', max_length=100)
        city = models.CharField(default='', max_length=100)
        state = models.CharField(default='', max_length=100)
        phone =  models.IntegerField(default=0)
        website = models.CharField(max_length=120, default='')
        width_field = models.IntegerField(default=0)
        height_field = models.IntegerField(default=0)
        image = models.ImageField(upload_to="profile_image", default="path/to/my/default/image.jpg")
        last_name = models.CharField(max_length=120, default='')
        email = models.CharField(max_length=120, default='')
        user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True, blank = True)

        def __unicode__(self):
            return self.name

**Результат:**

.. image:: _static/profile.png
  :target: _static/profile.png

**Класс userStripe**
====================

Состоит из следующих полей: user, stripe_id.

Методы:

* __unicode__ - то же самое, что и для класса profile, но рассчитанный в первую очередь на возвращение ID.
* stripeCallback - отвечает за создание Stripe ID и Stripe профиля пользователя.
* profileCallback - отвечает за изменения профиля пользователя и появление его в системе после регистрации.

Данные поля заполняются пользователями- администраторами приложения.

Листинг::

    class userStripe(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
        stripe_id = models.CharField(max_length = 200, null = True, blank = True)

        def __unicode__(self):
            # Если есть ID, преобразуй в его в строку:
            if self.stripe_id:
                return str(self.stripe_id)
            # Иначе верни имя пользователя:
            else:
                return self.user.username

        def stripeCallback(sender, request, user, **kwargs):
            user_stripe_account, created = userStripe.objects.get_or_create(user = user)

            # Если Stripe пользователя создан, появляется его профиль.
            if created:
                print(f'created for {user.username}')
            # Если ID системы stripe не существует, то используй email пользователя для его создания:
            if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id == '':
                new_stripe_id = stripe.Customer.create(email = user.email)
                user_stripe_account.stripe_id = new_stripe_id['id']
                user_stripe_account.save()

        def profileCallback(sender, request, user, **kwargs):
            userProfile, is_created = Profile.objects.get_or_create(user = user)

            # Если пользователь создан, появляется его профиль.
            if is_created:
                userProfile.name = user.username
                userProfile.save()

        user_logged_in.connect(stripeCallback)
        user_signed_up.connect(stripeCallback)
        user_signed_up.connect(profileCallback)

**Представления**
=================

Состоит из следующих полей: user, stripe_id.

Методы:

* home - подключение начальной страницы приложения.
* about - подключение страницы описания приложения.
* userProfile - функция подключения страницы профиля, которая появляется в меню навигации только после входа в профиль.

Листинг::

    def home(request):
        context = {}
        template = 'home.html'
        return render(request, template, context)

    def about(request):
        context = {}
        template = 'about.html'
        return render(request, template, context)

    # Декоратор, требующий обязательного входа в профиль:
    @login_required
    def userProfile(request):
        user = request.user
        context = {'user': user}
        template = 'profile.html'
        return render(request, template, context)

**Домашняя страница:**

.. image:: _static/home.png
  :target: _static/home.png

**Страница описания:**

.. image:: _static/about.png
  :target: _static/about.png

**Страница профиля:**

.. image:: _static/profile2.png
  :target: _static/profile2.png
