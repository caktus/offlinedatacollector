import datetime

from django.contrib.auth.models import User
from django.db import models


class Cleaning(models.Model):
    """An instance of a cleaning"""

    user = models.ForeignKey(User, related_name='cleanings')
    completed = models.BooleanField(
        help_text="Did you clean?",
        default=False
    )
    date = models.DateField(default=datetime.date.today)
