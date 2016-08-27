from django.contrib.auth.decorators import login_required
from django.db.models.expressions import RawSQL
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Challenge, SolveLog
from accounts.models import User


def ranking(request):
    age_group = int(request.GET.get('age', 0))
    if age_group == 0:
        qs = User.objects
    else:
        qs = User.objects.filter(age_type=age_group)
    if age_group == 3:
        users = qs\
            .annotate(score=RawSQL("""(
                COALESCE((SELECT SUM("challenges_challenge"."original_score") FROM "challenges_challenge"
                WHERE "challenges_challenge"."id" IN
                (SELECT "challenges_challenge_solvers"."challenge_id" FROM "challenges_challenge_solvers"
                WHERE "challenges_challenge_solvers"."user_id" = "accounts_user"."id")), 0) +
                COALESCE((SELECT SUM("challenges_challenge"."breakthrough_score") FROM "challenges_challenge"
                WHERE "challenges_challenge"."breakthrough_solver_id" = "accounts_user"."id"), 0))""",()))
    else:
        users = qs\
            .annotate(score=RawSQL("""(
                COALESCE((SELECT SUM("challenges_challenge"."score") FROM "challenges_challenge"
                WHERE "challenges_challenge"."id" IN
                (SELECT "challenges_challenge_solvers"."challenge_id" FROM "challenges_challenge_solvers"
                WHERE "challenges_challenge_solvers"."user_id" = "accounts_user"."id")), 0) +
                COALESCE((SELECT SUM("challenges_challenge"."breakthrough_score") FROM "challenges_challenge"
                WHERE "challenges_challenge"."breakthrough_solver_id" = "accounts_user"."id"), 0))""", ()))\
            # TODO: Subquery->Join
    users = users.order_by('-score').order_by('-solve_log__solved_at')  
    return render(request, 'ranking.html', {'users': users, 'age_group': age_group, 'age_types': User.Age.CHOICES[:3], 'current_age': age_group})


class ChallengeListView(ListView):
    model = Challenge
    context_object_name = 'challenges'

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category is None:
            return Challenge.objects.all()
        else:
            return Challenge.objects.filter(category=category)

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
    if request.method == "POST":
        input_answer = request.POST.get("answer")
        if input_answer == challenge.answer:
            SolveLog.objects.create(user=request.user, challenge=challenge, ip=get_client_ip(request))
            challenge.solvers.add(request.user)
            return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})
        else:
            return render(request, 'challenges/challenge_detail.html', {'challenge': challenge, 'error': 'Wrong Key', 'value': input_answer})
    else:
        return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})
