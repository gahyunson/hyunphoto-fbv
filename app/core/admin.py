from django.contrib import admin

from core import models


admin.site.register(models.User)
admin.site.register(models.Photos)
admin.site.register(models.Prices)
admin.site.register(models.Cart)
