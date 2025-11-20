from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'fullname', 'is_staff', 'is_active', 'id')
    search_fields = ('email', 'fullname')

admin.site.register(CustomUser, CustomUserAdmin)

