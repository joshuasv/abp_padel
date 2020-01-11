from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile

class ProfileInline(admin.TabularInline):
    model = Profile


class MyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'sex', 'dni')}
        ),
    )
    inlines = [ProfileInline]

admin.site.register(User, MyUserAdmin)
