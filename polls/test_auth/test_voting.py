from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from polls.models import Vote
from polls.test_auth.test_index import create_question


class VotingTest(TestCase):
    """Test on voting system."""

    def setUp(self):
        """Create user and model for test."""
        self.username = "HelloYeew"
        self.password = "password"
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        self.question = create_question("How is it?", 7)
        self.choice1 = self.question.choice_set.create(choice_text="Good")
        self.choice2 = self.question.choice_set.create(choice_text="Bad")
        self.voting_page = reverse("polls:vote", args=[self.question.id])

    def login(self):
        """Login user."""
        self.client.login(username=self.username, password=self.password)

    def test_voting_page_not_logged_in(self):
        """Test voting page not logged in."""
        vote_response = self.client.post(self.voting_page, data={"choice": self.choice1.id})
        login_redirect_url = f"{reverse('login')}?next={self.voting_page}"
        self.assertRedirects(vote_response, login_redirect_url)

    def test_voting_page_logged_in(self):
        """Test voting page logged in."""
        self.login()
        self.client.post(self.voting_page, data={"choice": self.choice1.id})
        self.assertEqual(Vote.objects.filter(choice__question=self.question, user=self.user).count(), 1)

    def test_voting_same_choice_many_times(self):
        """Test voting many times and the vote choice must be 1."""
        self.login()
        for i in range(5):
            self.client.post(self.voting_page, data={"choice": self.choice1.id})
        self.assertEqual(Vote.objects.filter(choice__question=self.question).count(), 1)
        self.assertEqual(Vote.objects.get(choice__question=self.question, user=self.user).choice, self.choice1)

    def test_voting_different_choice(self):
        """Test voting with changing to different choice."""
        self.login()
        self.client.post(self.voting_page, data={"choice": self.choice1.id})
        self.assertEqual(Vote.objects.filter(choice__question=self.question).count(), 1)
        self.assertEqual(Vote.objects.get(choice__question=self.question, user=self.user).choice, self.choice1)
        self.client.post(self.voting_page, data={"choice": self.choice2.id})
        self.assertEqual(Vote.objects.filter(choice__question=self.question).count(), 1)
        self.assertEqual(Vote.objects.get(choice__question=self.question, user=self.user).choice, self.choice2)
