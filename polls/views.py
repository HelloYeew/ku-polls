"""File for views class for polls app."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from .models import Question, Choice, Vote
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


class IndexView(generic.ListView):
    """The homepage that contain all polls questions."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Detail view for each question."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """When the poll closed, redirect user to index page with message."""
        self.object = self.get_object()
        if self.object.can_vote():
            return render(request, 'polls/detail.html', self.get_context_data())
        else:
            messages.error(request, "Voting is not allowed")
            return redirect('polls:index')


class ResultsView(generic.DetailView):
    """Showing poll result on that question."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Operation when user submit the result."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            user_vote = Vote.objects.get(choice__question=question, user=request.user)
            user_vote.choice = selected_choice
            user_vote.save()
        except Vote.DoesNotExist:
            Vote.objects.create(choice=selected_choice, user=request.user)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
