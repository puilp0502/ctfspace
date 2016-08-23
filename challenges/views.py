from django.contrib.auth.decorators import login_required
from django.db.models.expressions import RawSQL
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Challenge
from accounts.models import User


def ranking(request):
    age_group = request.GET.get('age', None)
    if age_group is None:
        qs = User.objects
    else:
        qs = User.objects.filter(age_type=age_group)
    users = qs\
        .annotate(score=RawSQL("""(
            COALESCE((SELECT SUM("challenges_challenge"."score") FROM "challenges_challenge"
            WHERE "challenges_challenge"."id" IN
            (SELECT "challenges_challenge_solvers"."challenge_id" FROM "challenges_challenge_solvers"
            WHERE "challenges_challenge_solvers"."user_id" = "accounts_user"."id")), 0) +
            COALESCE((SELECT SUM("challenges_challenge"."breakthrough_score") FROM "challenges_challenge"
            WHERE "challenges_challenge"."breakthrough_solver_id" = "accounts_user"."id"), 0))""", ()))\
        .order_by('-score')  # TODO: Subquery->Join
    return render(request, 'ranking.html', {'users': users, 'age_group': age_group})


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
    challenge = get_object_or_404(Challenge, pk=pk)
    if request.method == "POST":
        input_answer = request.POST.get("answer")
        if input_answer == challenge.answer:
            challenge.solvers.add(request.user)
            return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})
        else:
            return render(request, 'challenges/challenge_detail.html', {'challenge': challenge, 'error': 'Wrong Key', 'value': input_answer})
    else:
        return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})