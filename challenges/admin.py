from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Challenge, SolveLog


class ChallengeAdmin(ModelAdmin):
    class Meta:
        model = Challenge
    list_display = ['title', 'category', 'score', 'solvers_count', 'is_hidden']

    def solvers_count(self, obj):
        return obj.solvers.count()

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(SolveLog)
