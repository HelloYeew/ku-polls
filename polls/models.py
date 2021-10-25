"""File contain all database models for polls app."""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Polls question database models."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField(default=timezone.now() + datetime.timedelta(days=7))

    def __str__(self):
        """Return string on Question model as the question."""
        return self.question_text

    def was_published_recently(self):
        """Return True if the poll is already published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return True if current date is on or after question’s publication date."""
        return timezone.now() > self.pub_date

    def can_vote(self):
        """Return True if voting is currently allowed for this question."""
        return (timezone.now() > self.pub_date) and (timezone.now() < self.end_date)


class Choice(models.Model):
    """Choice database model for binding it with question model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return string on Choice model as the choice."""
        return self.choice_text

    @property
    def votes(self) -> int:
        """Return votes number for this choice"""
        return Vote.objects.filter(choice=self).count()


class Vote(models.Model):
    """Vote database model for binding it with question model."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        """Return string on Vote model as the vote."""
        return f"Vote by {self.user.username} for {self.choice.choice_text}"
