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
            (MIDDLE_S, "Middle School"),
            (HIGH_S, "High School"),
            (ADULT, "Adult"),
            (OTHER, "Others"),
        )

    objects = UserManager()

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=64, unique=True, null=False, blank=False, help_text="이메일 주소")
    is_staff = models.BooleanField(default=False, help_text="관리자 여부")
    is_active = models.BooleanField(default=True, help_text="활성화 여부")
    date_joined = models.DateTimeField(default=timezone.now)

    age_type = models.IntegerField(choices=Age.CHOICES, null=False, blank=False, default=Age.OTHER)
    name = models.CharField(max_length=20, null=False, help_text="닉네임")
    school = models.CharField(max_length=15, null=True, blank=True)

    last_solved_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'age_type']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def score(self):
        user = User.objects.filter(pk=self.pk)
        if self.age_type == User.Age.MIDDLE_S:
            qs = user.annotate(score=Sum('solved__middleschool_score'))
        elif self.age_type == User.Age.HIGH_S:
            qs = user.annotate(score=Sum('solved__highschool_score'))
        elif self.age_type == User.Age.ADULT:
            qs = user.annotate(score=Sum('solved__adult_score'))
        else:
            qs = user.annotate(score=Sum('solved__original_score'))
        score = qs[0].score
        if score is None:
            score = 0
        return score
