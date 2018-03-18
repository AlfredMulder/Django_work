from django.contrib import admin

# Register your models here.
from .models import Profile, userStripe

# Создание модели профиля администратора:
class profileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile

admin.site.register(Profile, profileAdmin)

# Создание модели профиля администратора Stripe:
class userStripeAdmin(admin.ModelAdmin):
    class Meta:
        model = userStripe

admin.site.register(userStripe, userStripeAdmin)
