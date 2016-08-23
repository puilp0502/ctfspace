from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import User


class CustomUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(UserAdmin):
    form = CustomUserForm
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('email',)
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password',
                       'is_staff', 'is_active', 'date_joined', 'last_login', 'age_type', 'name', 'school',
                       'score', )
        }),
    )
    readonly_fields = ['score']

    def score(self, obj):
        return obj.score()

    list_display = ('username', 'email', 'name', 'date_joined', 'last_login', 'age_type', 'score')

admin.site.register(User, CustomUserAdmin)
