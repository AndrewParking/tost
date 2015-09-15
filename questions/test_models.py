from django.test import TestCase
from account.models import Account
from .models import Question, Answer, Comment, Like


# ===========================================
# ================= Mixins ==================
# ===========================================


class ContentTypeTestMixin(object):

    def setUp(self):
        self.account = Account.objects.create_user(
            username='Andr',
            email='popow@tut.by',
            password='homm1994'
        )
        self.question = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=self.account
        )
        self.answer = Answer.objects.create(
            content='Ruby, no doubt',
            author=self.account,
            question=self.question
        )


# ===========================================
# ================= Tests ===================
# ===========================================


class QuestionModelTest(TestCase):

    def create_user(self):
        account = Account.objects.create_user(
            username='Andr',
            email='popow@tut.by',
            password='homm1994'
        )
        return account

    def test_manager_creates_question_instance(self):
        account = self.create_user()
        Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        quest = Question.objects.first()
        self.assertEqual(quest.summary, 'Programming language')
        self.assertEqual(quest.content, 'What programming language should I choose')
        self.assertEqual(quest.author, account)

    def test_save_creates_question_instance(self):
        account = self.create_user()
        quest = Question(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        quest.save()
        quest = Question.objects.first()
        self.assertEqual(quest.summary, 'Programming language')
        self.assertEqual(quest.content, 'What programming language should I choose')
        self.assertEqual(quest.author, account)

    def test_updates_data(self):
        account = self.create_user()
        quest = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        quest.summary = 'Something'
        quest.save()
        self.assertEqual(quest.summary, 'Something')

    def test_comments(self):
        account = self.create_user()
        quest = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        Comment.objects.create(
            author=account,
            content_object=quest,
            content='Some sweet words'
        )
        self.assertEqual(quest.comments.count(), 1)
        self.assertEqual(quest.comments.first().content, 'Some sweet words')

    def test_comments_count(self):
        account = self.create_user()
        quest = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        Comment.objects.create(
            author=account,
            content_object=quest,
            content='Some sweet words'
        )
        self.assertEqual(quest.comments_count, 1)

    def test_likes(self):
        account = self.create_user()
        quest = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        Like.objects.create(
            author=account,
            content_object=quest
        )
        self.assertEqual(quest.likes.count(), 1)
        self.assertEqual(quest.likes.first().author, account)

    def test_likes_count(self):
        account = self.create_user()
        quest = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        Like.objects.create(
            author=account,
            content_object=quest
        )
        self.assertEqual(quest.likes_count, 1)

    def test_str(self):
        account = self.create_user()
        quest = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=account
        )
        self.assertEqual(quest.__str__(), 'Programming language')


class AnswerModelTest(TestCase):

    def create_user(self):
        account = Account.objects.create_user(
            username='Andr',
            email='popow@tut.by',
            password='homm1994'
        )
        return account

    def create_question(self):
        acc = Account.objects.create(
            username='Andreww',
            email='popw@tut.by',
            password='homm1994'
        )
        quest = Question.objects.create(
            summary='Programming language',
            content='What programming language should I choose',
            author=acc
        )
        return quest

    def test_manager_creates_answer_instance(self):
        account = self.create_user()
        quest = self.create_question()
        Answer.objects.create(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        answ = Answer.objects.first()
        self.assertEqual(answ.content, 'Definitely it is python')
        self.assertEqual(answ.author, account)
        self.assertEqual(answ.question, quest)

    def test_save_creates_question_instance(self):
        account = self.create_user()
        quest = self.create_question()
        answ = Answer(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        answ.save()
        answ = Answer.objects.first()
        self.assertEqual(answ.content, 'Definitely it is python')
        self.assertEqual(answ.author, account)
        self.assertEqual(answ.question, quest)

    def test_updates_data(self):
        account = self.create_user()
        quest = self.create_question()
        answ = Answer.objects.create(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        answ.content = 'No, it is Java.'
        answ.save()
        self.assertEqual(answ.content, 'No, it is Java.')

    def test_comments(self):
        account = self.create_user()
        quest = self.create_question()
        answ = Answer.objects.create(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        Comment.objects.create(
            author=account,
            content_object=answ,
            content='Some sweet words'
        )
        self.assertEqual(answ.comments.count(), 1)
        self.assertEqual(answ.comments.first().content, 'Some sweet words')

    def test_comments_count(self):
        account = self.create_user()
        quest = self.create_question()
        answ = Answer.objects.create(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        Comment.objects.create(
            author=account,
            content_object=answ,
            content='Some sweet words'
        )
        self.assertEqual(answ.comments_count, 1)

    def test_likes(self):
        account = self.create_user()
        quest = self.create_question()
        answ = Answer.objects.create(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        Like.objects.create(
            author=account,
            content_object=answ
        )
        self.assertEqual(answ.likes.count(), 1)
        self.assertEqual(answ.likes.first().author, account)

    def test_likes_count(self):
        account = self.create_user()
        quest = self.create_question()
        answ = Answer.objects.create(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        Like.objects.create(
            author=account,
            content_object=answ
        )
        self.assertEqual(answ.likes_count, 1)

    def test_str(self):
        account = self.create_user()
        quest = self.create_question()
        answ = Answer.objects.create(
            content='Definitely it is python',
            author=account,
            question=quest
        )
        self.assertEqual(answ.__str__(), 'Definitely it is python')


class CommentModelTest(ContentTypeTestMixin, TestCase):

    def test_manager_creates_instance(self):
        Comment.objects.create(
            content='Some sweet words',
            author=self.account,
            content_object=self.answer
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.account)
        self.assertEqual(Comment.objects.first().content, 'Some sweet words')

    def test_save_creates_instance(self):
        comment = Comment(
            content='Some sweet words',
            author=self.account,
            content_object=self.answer
        )
        comment.save()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author, self.account)
        self.assertEqual(Comment.objects.first().content, 'Some sweet words')

    def test_updates_instance(self):
        comment = Comment.objects.create(
            content='Some sweet words',
            author=self.account,
            content_object=self.answer
        )
        comment.content = 'Some really bad words'
        comment.save()
        self.assertEqual(comment.content, 'Some really bad words')

    def test_str(self):
        comment = Comment.objects.create(
            content='Some sweet words',
            author=self.account,
            content_object=self.answer
        )
        self.assertEqual(comment.__str__(), 'Some sweet words')


class LikeModelTest(ContentTypeTestMixin, TestCase):

    def test_manager_creates_instance(self):
        Like.objects.create(
            author=self.account,
            content_object=self.answer
        )
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().author, self.account)

    def test_save_creates_instance(self):
        like = Like(
            author=self.account,
            content_object=self.answer
        )
        like.save()
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.first().author, self.account)

    def test_updates_instance(self):
        like = Like.objects.create(
            author=self.account,
            content_object=self.answer
        )
        like.content_object = self.question
        like.save()
        self.assertEqual(like.content_object, self.question)

    def test_str(self):
        like = Like.objects.create(
            author=self.account,
            content_object=self.answer
        )
        self.assertEqual(like.__str__(), '%s: %s' % (like.author.username, like.created_at))