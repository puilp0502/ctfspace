from math import exp
from django.db import models
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.models import User


class Challenge(models.Model):
    class Category:
        WEB = 1
        Pwnable = 2
        Reversing = 3
        Forensic = 4
        Crypto = 5
        Misc = 0
        choices = (
            (WEB, "WEB"),
            (Pwnable, "PWNABLE"),
            (Reversing, "REVERSING"),
            (Forensic, "F0RENSIC"),
            (Crypto, "CRYPT0"),
            (Misc, "MISC"),
        )
    title = models.CharField(max_length=50, null=False, unique=True, blank=False)
    description = models.TextField()
    category = models.IntegerField(choices=Category.choices, default=Category.Misc)
    file = models.FileField(null=True, blank=True)
    answer = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    original_score = models.IntegerField(help_text="기본 점수")
    score = models.IntegerField(blank=True, help_text="가중치 조절된 점수: 자동조정")
    solvers = models.ManyToManyField(User, blank=True, related_name='solved')

    def __str__(self):
        return "<Challenge "+self.title+">"


@receiver(pre_save, sender=Challenge)
def pre_save(sender, instance, *args, **kwargs):
    if not instance.score:
        instance.score = instance.original_score


def calculate_score(original_score, solver_count):
    """
    Calculate score based on logarithmic Sigmoid function; Check https://www.desmos.com/calculator/vl5yx8rsq6
    :param original_score: original score of the challenge
    :param solver_count: the number of solver(s)
    :return: calculated challenge's score
    """
    if solver_count > 0:
        k = 80  # Maximum solver; after this point, the score will remain same.
        v = 0.1  # Minimum score percentage
        score = (1-v) / (1 + exp((12/k) * (solver_count-(k+1)/2))) + v
        score *= original_score
        return int(score)
    else:
        return original_score


def update_score(sender, **kwargs):
    print("update_score called")
    print(sender, kwargs)
    if kwargs.get('action') in ('post_add', 'post_remove'):
        if not kwargs.get('reverse'):
            challenge = kwargs.get('instance')
            challenge.score = calculate_score(challenge.original_score, challenge.solvers.count())
            challenge.save()
            User.objects.filter(pk__in=kwargs.get('pk_set')).update(last_solved_at=timezone.now())
        else:
            challenges = Challenge.objects.filter(pk__in=kwargs.get('pk_set'))
            for challenge in challenges:
                challenge.score = calculate_score(challenge.original_score, challenge.solvers.count())
                challenge.save()
            solver = kwargs.get('instance')
            solver.last_solved_at = timezone.now()

m2m_changed.connect(update_score, sender=Challenge.solvers.through)


class SolveLog(models.Model):
    solved_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return "SolveLog User '"+self.user.name+"' - "+self.challenge.title+" @ "+self.ip
