from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Account


class TestAccountModel(TestCase):

    def create_ordinary_account(self):
        account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        return account

    def test_save_creates_ordinary_account(self):
        account = Account(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        account.save()
        data = Account.objects.first()
        self.assertEqual(data.username, 'Andrew')
        self.assertEqual(data.email, 'pop@tut.by')

    def test_creates_instance_with_valid_data(self):
        data = self.create_ordinary_account()
        self.assertEqual(data.username, 'Andrew')
        self.assertEqual(data.email, 'pop@tut.by')

    def test_creates_superuser_with_valid_data(self):
        Account.objects.create_superuser(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        data = Account.objects.first()
        self.assertEqual(data.username, 'Andrew')
        self.assertEqual(data.email, 'pop@tut.by')
        self.assertTrue(data.is_admin)
        self.assertTrue(data.is_staff)

    def test_raises_error_without_email(self):
        self.assertRaises(
            TypeError,
            Account.objects.create_user,
            username='Andrew',
            password='homm1994'
        )

    def test_save_fails_without_email(self):
        account = Account(
            username='hen',
            password='homm1995'
        )
        self.assertRaises(
            ValidationError,
            account.save
        )

    def test_save_fails_without_username(self):
        account = Account(
            email='pop@tut.by',
            password='homm1994'
        )
        self.assertRaises(
            ValidationError,
            account.save
        )

    def test_raises_error_without_username(self):
        self.assertRaises(
            TypeError,
            Account.objects.create_user,
            email='pop@tut.by',
            password='homm1994'
        )

    def test_updates_instance(self):
        account = self.create_ordinary_account()
        account.username = 'Andzei'
        account.email = 'andrew@mail.ru'
        account.save()
        self.assertEqual(account.username, 'Andzei')
        self.assertEqual(account.email, 'andrew@mail.ru')

    def test_str(self):
        account = self.create_ordinary_account()
        self.assertEqual(account.__str__(), 'Andrew')

    def test_get_short_name(self):
        account = self.create_ordinary_account()
        self.assertEqual(account.get_short_name(), 'Andrew')

    def test_get_full_name(self):
        account = self.create_ordinary_account()
        self.assertEqual(account.get_full_name(), 'Andrew')