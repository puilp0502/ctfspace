from django.shortcuts import render

from challenges.models import Challenge
from notice.models import Notice


def dashboard(request):
    challenges = Challenge.objects.all().order_by('-created_at')[:5]
    posts = Notice.objects.all().order_by('-created_at')[:3]
    return render(request, 'dashboard.html', {'challenges': challenges, 'posts': posts})