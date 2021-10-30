"""Template tag for using in detail template"""

from django import template
from polls.models import Vote

register = template.Library()


def get_choice_result(choice, user):
    """Return the value that use when render radio button that is user already vote this choice or not.

    Args:
        choice: Choice object
        user: User object

    Returns:
        Value use when render the radio choice list.
    """
    if Vote.objects.filter(choice=choice, user=user).exists():
        return "checked"
    return None


register.filter('get_choice_result', get_choice_result)
