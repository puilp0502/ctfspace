from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.db.models import Sum, F
from django.db.models.expressions import RawSQL
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    class Age:
        MIDDLE_S = 1
        HIGH_S = 2
        ADULT = 3
        OTHER = 4
        CHOICES = (
            (MIDDLE_S, "중등부"),
            (HIGH_S, "고등부"),
            (ADULT, "성인"),
            (OTHER, "기타"),
        )

    objects = UserManager()

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=64, unique=True, null=False, blank=False, help_text="이메일 주소")
    is_staff = models.BooleanField(default=False, help_text="관리자 여부")
    is_active = models.BooleanField(default=True, help_text="활성화 여부")
    date_joined = models.DateTimeField(default=timezone.now)

    age_type = models.IntegerField(choices=Age.CHOICES, null=False, blank=False, default=Age.OTHER)
    name = models.CharField(max_length=10, null=False, help_text="이름")
    school = models.CharField(max_length=15, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'age_type']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def score(self):
        qs = User.objects.filter(pk=self.pk)\
            .annotate(score=RawSQL("""(
            COALESCE((SELECT SUM("challenges_challenge"."score") FROM "challenges_challenge"
            WHERE "challenges_challenge"."id" IN
            (SELECT "challenges_challenge_solvers"."challenge_id" FROM "challenges_challenge_solvers"
            WHERE "challenges_challenge_solvers"."user_id" = "accounts_user"."id")), 0) +
            COALESCE((SELECT SUM("challenges_challenge"."breakthrough_score") FROM "challenges_challenge"
            WHERE "challenges_challenge"."breakthrough_solver_id" = "accounts_user"."id"), 0))""", ()))  # TODO: Subquery->Join
        score = qs[0].score
        if score is None:
            score = 0
        return score
