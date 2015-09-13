from django.test import TestCase
from .forms import CreateAccountForm, UpdateAccountForm


class CreateAccountFormTest(TestCase):

    def test_with_empty_data(self):
        form = CreateAccountForm({})
        self.assertFalse(form.is_valid())

    def test_with_valid_data(self):
        form = CreateAccountForm({
            'username': 'Andrew',
            'email': 'pop@tut.by',
            'tagline': 'We don\'t saw!',
            'password1': 'homm1994',
            'password2': 'homm1994'
        })
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form = CreateAccountForm({
            'username': 'A'*150,
            'email': 'pop@tut.by',
            'password1': 'homm1994',
            'password2': 'homm1994'
        })
        self.assertFalse(form.is_valid())

    def test_with_different_passwords(self):
        form = CreateAccountForm({
            'username': 'Andrew',
            'email': 'pop@tut.by',
            'password1': 'homm1994',
            'password2': 'homm1995'
        })
        self.assertFalse(form.is_valid())


class UpdateAccountFormTest(TestCase):

    def test_with_empty_data(self):
        form = UpdateAccountForm({})
        self.assertFalse(form.is_valid())

    def test_with_valid_data(self):
        form = UpdateAccountForm({
            'username': 'Andrew',
            'email': 'pop@mail.ru',
            'tagline': 'Hear me roar!'
        })
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form = UpdateAccountForm({
            'username': 'Andrew',
            'tagline': 'Hear me roar!'
        })
        self.assertFalse(form.is_valid())
