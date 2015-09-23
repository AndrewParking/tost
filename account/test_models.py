from django.test import TestCase
from django.core.exceptions import ValidationError
from questions.models import Question, Answer, Comment, Like
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

    def test_questions_count(self):
        account = self.create_ordinary_account()
        question1 = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        question2 = Question.objects.create(
            summary='Some other summary',
            content='Some other content',
            author=account
        )
        self.assertEqual(account.questions_count, 2)

    def test_answers_count(self):
        account = self.create_ordinary_account()
        question = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        answer1 = Answer.objects.create(
            content='Some content',
            question=question,
            author=account
        )
        answer2 = Answer.objects.create(
            content='Some other content',
            question=question,
            author=account
        )
        self.assertEqual(account.answers_count, 2)

    def test_solution_percent(self):
        account = self.create_ordinary_account()
        question = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        answer1 = Answer.objects.create(
            content='Some content',
            question=question,
            author=account,
            solution=True
        )
        answer2 = Answer.objects.create(
            content='Some other content',
            question=question,
            author=account
        )
        self.assertEqual(account.solution_percent, 50)

    def test_reverse_questions(self):
        account = self.create_ordinary_account()
        question1 = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        question2 = Question.objects.create(
            summary='Some other summary',
            content='Some other content',
            author=account
        )
        questions = account.own_questions.all()
        self.assertEqual(questions.count(), 2)
        self.assertEqual(questions.first(), question1)
        self.assertEqual(questions.last(), question2)

    def test_reverse_answers(self):
        account = self.create_ordinary_account()
        question = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        answer1 = Answer.objects.create(
            content='Some content',
            question=question,
            author=account
        )
        answer2 = Answer.objects.create(
            content='Some other content',
            question=question,
            author=account
        )
        answers = account.own_answers.all()
        self.assertEqual(answers.count(), 2)
        self.assertEqual(answers.first(), answer1)
        self.assertEqual(answers.last(), answer2)

    def test_reverse_comments(self):
        account = self.create_ordinary_account()
        question = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        comment1 = Comment.objects.create(
            content='Some comment',
            content_object=question,
            author=account
        )
        comment2 = Comment.objects.create(
            content='Some other content',
            content_object=question,
            author=account
        )
        comments = account.comments.all()
        self.assertEqual(comments.count(), 2)
        self.assertEqual(comments.first(), comment1)
        self.assertEqual(comments.last(), comment2)

    def test_reverse_likes(self):
        account = self.create_ordinary_account()
        question1 = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        question2 = Question.objects.create(
            summary='Some summary',
            content='Some content',
            author=account
        )
        like1 = Like.objects.create(
            content_object=question1,
            author=account
        )
        like2 = Like.objects.create(
            content_object=question2,
            author=account
        )
        likes = account.likes.all()
        self.assertEqual(likes.count(), 2)
        self.assertEqual(likes.first(), like1)
        self.assertEqual(likes.last(), like2)
