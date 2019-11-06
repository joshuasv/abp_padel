from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile

class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'username', 'email', 'dni', 'sex', 'password']
    inlines = [ProfileInline]

admin.site.register(User, UserAdmin)
