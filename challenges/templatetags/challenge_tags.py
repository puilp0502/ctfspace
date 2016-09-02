from django import template

from accounts.models import User

register = template.Library()


@register.simple_tag
def get_challenge_score(challenge, age_type):
    if age_type == User.Age.MIDDLE_S:
        return challenge.middleschool_score
    elif age_type == User.Age.HIGH_S:
        return challenge.highschool_score
    else:
        return challenge.adult_score
