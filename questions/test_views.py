from django.test import TestCase
from django.core.urlresolvers import reverse
from account.models import Account


class QuestionsListPageViewTest(TestCase):

    def create_user(self):
        account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        return account

    def test_redirects_anon_user(self):
        response = self.client.get(reverse('questions:questions_list'))
        self.assertRedirects(response, reverse('account:sign_in'))

    def test_renders_right_template(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(reverse('questions:questions_list'))
        self.assertTemplateUsed(response, 'questions/questions_list.html')
