from django.contrib import admin

# Register your models here.
from .models import Profile
#Добавление нового профиля в админку

class profileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile

admin.site.register(Profile, profileAdmin)
