from django.db import models

# Create your models here.
#Создание модели профиля пользователя.
class Profile(models.Model):
    #Добавление новых полей: name, description, location, job.
    name = models.CharField(max_length=120)
    description = models.TextField(default='description default text')
    location = models.CharField(max_length=120, default='My location default', blank=True, null=True)
    job = models.CharField(max_length=120, null=True)

    def __unicode__(self):
        return self.name
