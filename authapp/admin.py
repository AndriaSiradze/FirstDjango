from django.contrib import admin

from authapp.models import CustomUser


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_active', 'email', 'date_joined', 'last_login']
    ordering = ('-date_joined',)

