from django.contrib import admin

# Register your models here.
from account.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']
    readonly_fields = ('location_time',)
    fieldsets = (
        (None, {'fields': (
            ('email', 'username'),
            ('first_name', 'last_name'),
            ('is_verified', 'is_active'),
            ('is_staff', 'is_superuser'),
            ('lat', 'lng'),
            'image',
            'age',
            'gender',
            ('location_time',),
            'last_login',

        )}),)


admin.site.register(User, UserAdmin)
