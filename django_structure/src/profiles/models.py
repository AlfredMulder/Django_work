from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up
import stripe

stripe_api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
# Создание модели профиля пользователя админки:
class Profile(models.Model):
    # Добавление новых полей: name, description, location, job:
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    description = models.TextField(default='description default text')
    street = models.CharField(default='', max_length=100)
    city = models.CharField(default='', max_length=100)
    state = models.CharField(default='', max_length=100)
    phone =  models.IntegerField(default=0)
    website = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    job = models.CharField(max_length=120, null=True)
    image = models.ImageField(upload_to="profile_image", height_field=800 , width_field=600)
    # Создание профиля пользователя:

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null = True, blank = True)


    def __unicode__(self):
        return self.name

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
