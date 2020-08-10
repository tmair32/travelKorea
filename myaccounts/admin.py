from django.contrib import admin
from .models import MyUser

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'last_login']

admin.site.register(MyUser, UserAdmin)