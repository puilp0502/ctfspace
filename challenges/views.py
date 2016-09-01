import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import Http404
from django.urls import reverse

from .models import Challenge, SolveLog
from accounts.models import User

logger = logging.getLogger('root')


def ranking(request):
    age_group = int(request.GET.get('age', 0))
    qs = User.objects.exclude(age_type=4)  # Remove Administration Account from Ranking
    if age_group != 0:
        qs = qs.filter(age_type=age_group)

    if age_group == 3:  # Display original score for non-student competitors
        users = qs\
            .annotate(score=Sum('solved__original_score'))
    else:
        users = qs\
            .annotate(score=Sum('solved__score'))
    users = users.exclude(score=0).order_by('-score', 'last_solved_at')
    return render(request, 'ranking.html', {'users': users, 'age_group': age_group, 'age_types': User.Age.CHOICES[:3], 'current_age': age_group})


class ChallengeListView(ListView):
    model = Challenge
    context_object_name = 'challenges'

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category is None:
            return Challenge.objects.filter(is_hidden=False)
        else:
            return Challenge.objects.filter(is_hidden=False, category=category)

    def get_context_data(self, **kwargs):
        context = super(ChallengeListView, self).get_context_data(**kwargs)
        context['categories'] = Challenge.Category.choices
        context['current_category'] = int(self.request.GET.get('category', -1))
        return context


@login_required
def challenge_detail_view(request, pk):
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            return ip

    challenge = get_object_or_404(Challenge, pk=pk)
    if challenge.is_hidden:
        raise Http404("No Challenge matches this given query")
    if request.method == "POST":
        input_answer = request.POST.get("answer").strip()
        if input_answer == challenge.answer.strip():
            if not request.user.is_staff:
                SolveLog.objects.create(user=request.user, challenge=challenge, ip=get_client_ip(request))
                challenge.solvers.add(request.user)
                logger.info("User {} successfully solved challenge {}.".format(request.user.username, challenge.title),
                            exc_info=False, extra={'request': request})
                return render(request, 'alert.html', {'message': 'Congratulations!\nYou solved the challenge!', 'url': reverse('challenge', args=[challenge.pk])})
            else:
                return render(request, 'alert.html',
                      {'message': 'You solved the problem, but it will not be saved because you\'re a staff.',
                       'url': reverse('challenge', args=[challenge.pk])})
        else:
            logger.info("User {} failed to solve challenge {}(with key {}).".format(request.user.username,
                                                                                    challenge.title,
                                                                                    input_answer),
                        exc_info=False, extra={'request': request})
            return render(request, 'challenges/challenge_detail.html', {'challenge': challenge, 'error': 'Wrong Key', 'value': input_answer})
    else:
        return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})
