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


class ProfileViewTest(CreateValidUserMixin, TestCase):

    def test_redirects_anon_user(self):
        account = self.create_user()
        response = self.client.get(reverse('account:profile', args=(account.id,)))
        self.assertRedirects(response, reverse('account:sign_in'))

    def test_renders_right_template(self):
        account = self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(reverse('account:profile', args=(account.id,)))
        self.assertTemplateUsed(response, 'account/profile.html')


class SignUpViewTest(CreateValidUserMixin, TestCase):

    def test_redirects_authed_user(self):
        account = self.create_user()
        self.client.login(username=account.username, password='homm1994')
        response = self.client.get(reverse('account:sign_up'))
        self.assertRedirects(response, reverse('account:profile', args=(account.id,)))

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
        account = Account.objects.last()
        self.assertRedirects(response, reverse('account:profile', args=(account.id,)))

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


class SignInViewTest(CreateValidUserMixin, TestCase):

    def test_redirects_authed_user(self):
        account = self.create_user()
        self.client.login(username=account.username, password='homm1994')
        response = self.client.get(reverse('account:sign_in'))
        self.assertRedirects(response, reverse('account:profile', args=(account.id,)))

    def test_renders_right_template(self):
        response = self.client.get(reverse('account:sign_in'))
        self.assertTemplateUsed(response, 'account/sign_in.html')

    def test_logs_user_in_after_valid_post(self):
        self.create_user()
        self.client.post(reverse('account:sign_in'), {
            'username': 'Andrew',
            'password': 'homm1994'
        })
        self.assertIn('_auth_user_id', self.client.session)

    def test_redirects_after_valid_post(self):
        account = self.create_user()
        response = self.client.post(reverse('account:sign_in'), {
            'username': 'Andrew',
            'password': 'homm1994'
        })
        self.assertRedirects(response, reverse('account:profile', args=(account.id,)))

    def test_renders_template_after_invalid_post(self):
        response = self.client.post(reverse('account:sign_in'), {
            'username': 'Andrew',
            'password': 'homm1994'
        })
        self.assertTemplateUsed(response, 'account/sign_in.html')


class UpdateAccountViewTest(CreateValidUserMixin, TestCase):

    def test_redirects_anon_user(self):
        response = self.client.get(reverse('account:update_account'))
        self.assertRedirects(response, reverse('account:sign_in'))

    def test_renders_right_template(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(reverse('account:update_account'))
        self.assertTemplateUsed(response, 'account/update_account.html')

    def test_modifies_data_after_valid_post(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        self.client.post(reverse('account:update_account'), {
            'username': 'Andzei',
            'email': 'pop@tut.by',
            'password': 'homm1994',
        })
        account = Account.objects.last()
        self.assertEqual(account.username, 'Andzei')

    def test_redirects_after_valid_post(self):
        account = self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.post(reverse('account:update_account'), {
            'username': 'Andzei',
            'email': 'pop@tut.by',
            'password': 'homm1994',
        })
        self.assertRedirects(response, reverse('account:profile', args=(account.id,)))

    def test_renders_template_after_invalid_post(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.post(reverse('account:update_account'), {
            'username': 'A'*200,
        })
        self.assertTemplateUsed(response, 'account/update_account.html')

    def test_no_data_change_after_invalid_post(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        self.client.post(reverse('account:update_account'), {
            'username': 'A'*200,
        })
        account = Account.objects.last()
        self.assertEqual(account.username, 'Andrew')