from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'created_at', 'password')


admin.site.register(User, UserAdmin)
