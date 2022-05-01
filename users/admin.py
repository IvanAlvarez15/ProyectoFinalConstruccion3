from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'first_name', 'email', 'check_unity', 'is_staff', 'is_active',)
    list_display = ('username', 'first_name', 'email', 'check_unity', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'status', 'check_unity', 'first_name','last_name', 'gender', 'date_joined', 'country','birthday','password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
            # 'fields': ('username', 'gender', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
