from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils import timezone

from .models import Challenge, SolveLog


class ChallengeAdmin(ModelAdmin):
    class Meta:
        model = Challenge
    list_display = ['title', 'category', 'middleschool_score', 'highschool_score', 'adult_score',
                    'solvers_count', 'is_hidden']

    def solvers_count(self, obj):
        return obj.solvers.count()

    def mark_hidden(self, request, queryset):
        queryset.update(is_hidden=True)
    mark_hidden.short_description = "Mark selected challenges as hidden"

    def mark_visible(self, request, queryset):
        queryset.update(is_hidden=False)
        queryset.update(created_at=timezone.now())
    mark_visible.short_description = "Mark selected challenges as visible"

    actions = ModelAdmin.actions + [mark_hidden, mark_visible]

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(SolveLog)
