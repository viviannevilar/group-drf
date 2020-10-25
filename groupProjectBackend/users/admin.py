
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'id','email']

admin.site.register(CustomUser,CustomUserAdmin)

# Register your models here.
