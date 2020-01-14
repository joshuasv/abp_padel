from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import User, Profile

class ProfileInline(admin.TabularInline):
    model = Profile


class MyUserAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'sex', 'dni')}),
    )

    inlines = [ProfileInline]


admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
