from django.contrib import admin
from Agent import models

# Register your models here.

admin.site.register(models.Type)
admin.site.register(models.House)
admin.site.register(models.House_Image)
admin.site.register(models.HousePayment)