"""File for adding models to admin page."""

from django.contrib import admin
from polls.models import Choice, Question

admin.site.register(Question)
admin.site.register(Choice)
