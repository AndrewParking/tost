from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Account


# =======================================================
# ======================= Mixins ========================
# =======================================================


class CreateValidUserMixin(object):

    def create_user(self):
        account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        return account

# =======================================================
# ======================= Views =========================
# =======================================================


class SignUpViewTest(CreateValidUserMixin, TestCase):

    def test_redirects_authed_user(self):
        account = self.create_user()
        self.client.login(username=account.username, password='homm1994')
        response = self.client.get(reverse('account:sign_up'))
        self.assertRedirects(response, '/')  # TODO: Change it

    def test_renders_right_template_to_anon_user(self):
        response = self.client.get(reverse('account:sign_up'))
        self.assertTemplateUsed(response, 'account/sign_up.html')

    def test_creates_user_after_valid_post(self):
        self.client.post(reverse('account:sign_up'), {
            'username': 'Andrew',
            'email': 'pop@tut.by',
            'password1': 'homm1994',
            'password2': 'homm1994'
        })
        account = Account.objects.first()
        self.assertEqual(account.username, 'Andrew')
        self.assertEqual(account.email, 'pop@tut.by')

    def test_logs_user_in_after_valid_post(self):
        self.client.post(reverse('account:sign_up'), {
            'username': 'Andrew',
            'email': 'pop@tut.by',
            'password1': 'homm1994',
            'password2': 'homm1994'
        })
        self.assertIn('_auth_user_id', self.client.session)

    def test_redirects_after_valid_post(self):
        response = self.client.post(reverse('account:sign_up'), {
            'username': 'Andrew',
            'email': 'pop@tut.by',
            'password1': 'homm1994',
            'password2': 'homm1994'
        })
        self.assertRedirects(response, '/')  # TODO: And this are to be changed too

    def test_renders_template_after_invalid_post(self):
        response = self.client.post(reverse('account:sign_up'), {
            'username': 'Andrew',
            'email': 'popow@mail.ru',
            'password1': 'homm1004',
            'password2': '4001mmoh'
        })
        self.assertTemplateUsed(response, 'account/sign_up.html')

    def test_no_new_user_after_invalid_post(self):
        self.client.post(reverse('account:sign_up'), {
            'username': 'Andrew',
            'email': 'popow@mail.ru',
            'password1': 'homm1004',
            'password2': '4001mmoh'
        })
        self.assertEqual(Account.objects.count(), 0)
