from django.contrib import admin
from .models import CustomUser, Organisation, CustomUserManager

admin.site.register(CustomUser)
admin.site.register(Organisation)