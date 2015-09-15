from django.contrib import admin
from .models import Account

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('required', {
            'fields': ['username', 'email']
        }),
        ('unnecessary', {
            'fields': ['tagline', 'description', 'photo'],
            'classes': ['collapse']
        }),
    ]
    list_display = ('username', 'email', 'created_at')
    filter_by = ['created_at']


admin.site.register(Account, AccountAdmin)
