from django.shortcuts import render

from challenges.models import Challenge, SolveLog
from notice.models import Notice


def dashboard(request):
    challenges = Challenge.objects.filter(is_hidden=False).order_by('-created_at')[:5]
    posts = Notice.objects.all().order_by('-created_at')[:3]
    solvers = SolveLog.objects.all().order_by('-solved_at')[:5]
    return render(request, 'dashboard.html', {'challenges': challenges, 'posts': posts, 'solvers': solvers})
