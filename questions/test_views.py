from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import Account
from .models import Tag, Question, Answer, Comment, Like


class BaseQuestionsListViewTest(object):

    def create_user(self):
        account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        return account

    def test_redirects_anon_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('account:sign_in'))

    def test_renders_right_template(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'questions/questions_list.html')

    def test_renders_right_template_with_search_param(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(self.url + '?q=how')
        self.assertTemplateUsed(response, 'questions/questions_list.html')

    def test_renders_right_template_with_page_param(self):
        self.create_user()
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(self.url + '?page=1')
        self.assertTemplateUsed(response, 'questions/questions_list.html')


class LatestQuestionsViewTest(BaseQuestionsListViewTest, TestCase):
    url = reverse('questions:questions_latest')


class BestQuestionsListViewTest(BaseQuestionsListViewTest, TestCase):
    url = reverse('questions:questions_best')


class UnansweredQuestionsListViewTest(BaseQuestionsListViewTest, TestCase):
    url = reverse('questions:questions_unanswered')


class ByTagIdQuestionsListViewTest(BaseQuestionsListViewTest, TestCase):
    url = reverse('questions:questions_by_tag_id', args=(1,))        

    def setUp(self):
        Tag.objects.create(name='test_tag')


class QuestionsDetailViewTest(TestCase):

    def setUp(self):
        self.account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        self.question = Question.objects.create(
            summary='Some title',
            content='Some text',
            author=self.account
        )


    def test_redirects_anon_user(self):
        response = self.client.get(reverse('questions:questions_detail', args=(self.question.id,)))
        self.assertRedirects(response, reverse('account:sign_in'))

    def test_renders_right_template(self):
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(reverse('questions:questions_detail', args=(self.question.id,)))
        self.assertTemplateUsed(response, 'questions/questions_detail.html')


class AddQuestionViewTest(TestCase):

    def setUp(self):
        self.account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        self.tag = Tag.objects.create(name='test_tag')

    def test_redirects_anon_user_get(self):
        response = self.client.get(reverse('questions:add_question'))
        self.assertRedirects(response, reverse('account:sign_in'))

    def test_renders_right_template(self):
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.get(reverse('questions:add_question'))
        self.assertTemplateUsed(response, 'questions/add_question.html')

    def test_redirects_anon_user_post(self):
        response = self.client.post(reverse('questions:add_question'), {
            'summary': 'Anon summary',
            'content': 'Anon content',
            'tags': [self.tag],
        })
        self.assertRedirects(response, reverse('account:sign_in'))

    def test_data_remains_untouched_after_anon_post(self):
        self.client.post(reverse('questions:add_question'), {
            'summary': 'Anon summary',
            'content': 'Anon content',
            'tags': [self.tag.id],
        })
        self.assertEqual(Question.objects.count(), 0)

    def test_modifies_data_after_authed_post(self):
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.post(reverse('questions:add_question'), {
            'summary': 'Anon summary',
            'content': 'Anon content',
            'tags': [self.tag.id],
        })
        question = Question.objects.last()
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(question.summary, 'Anon summary')
        self.assertEqual(question.content, 'Anon content')

    def test_redirects_after_authed_post(self):
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.post(reverse('questions:add_question'), {
            'summary': 'Anon summary',
            'content': 'Anon content',
            'tags': [self.tag.id],
        })
        self.assertRedirects(response, reverse('questions:questions_latest'))

    def test_rerenders_template_after_invalid_data(self):
        self.client.login(username='Andrew', password='homm1994')
        response = self.client.post(reverse('questions:add_question'), {
            'summary': 'A'*500,
            'content': 'Anon content',
            'tags': [self.tag],
        })
        self.assertTemplateUsed(response, 'questions/add_question.html')

    def test_data_remains_untouched_after_invalid_post(self):
        self.client.login(username='Andrew', password='homm1994')
        self.client.post(reverse('questions:add_question'), {
            'summary': 'A'*500,
            'content': 'Anon content',
            'tags': [self.tag],
        })
        self.assertEqual(Question.objects.count(), 0)


class QuestionsViewSetTest(APITestCase):

    def setUp(self):
        self.account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        self.foreign_account = Account.objects.create_user(
            username='Andri',
            email='popow@mail.ru',
            password='homm1994'
        )
        self.question = Question.objects.create(
            summary='Some title',
            content='Some text',
            author=self.account
        )

    def test_list_returns_403_to_anon_user(self):
        response = self.client.get(reverse('questions:questions-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_returns_data_to_authed_user(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.get(reverse('questions:questions-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['summary'], self.question.summary)
        self.assertEqual(response.data[0]['content'], self.question.content)

    def test_list_returns_403_to_anon_user_post(self):
        response = self.client.post(reverse('questions:questions-list'), {
            'summary': 'Question heading',
            'content': 'Question content',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_returns_201_after_authed_post(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.post(reverse('questions:questions-list'), {
            'summary': 'Question heading',
            'content': 'Question content',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_creates_instance_after_authed_post(self):
        self.client.force_authenticate(user=self.account)
        self.client.post(reverse('questions:questions-list'), {
            'summary': 'Question heading',
            'content': 'Question content',
        })
        questions = Question.objects.all()
        self.assertEqual(questions.count(), 2)
        self.assertEqual(questions.last().summary, 'Question heading')
        self.assertEqual(questions.last().content, 'Question content')

    def test_list_returns_400_after_invalid_post(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.post(reverse('questions:questions-list'), {
            'summary': 'Question heading'*500,
            'content': 'Question content',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_data_remains_untouched_after_invalid_post(self):
        self.client.force_authenticate(user=self.account)
        self.client.post(reverse('questions:questions-list'), {
            'summary': 'Question heading'*500,
            'content': 'Question content',
        })
        self.assertEqual(Question.objects.count(), 1)

    def test_detail_returns_403_to_anon_get(self):
        response = self.client.get(reverse('questions:questions-detail', args=(self.question.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_returns_data_to_authed_get(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.get(reverse('questions:questions-detail', args=(self.question.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['summary'], self.question.summary)

    def test_detail_returns_403_to_anon_put(self):
        response = self.client.put(reverse('questions:questions-detail', args=(self.question.id,)), {
            'summary': 'Question heading',
            'content': 'Question content',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_returns_403_to_foreign_put(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.put(reverse('questions:questions-detail', args=(self.question.id,)), {
            'summary': 'Another question heading',
            'content': 'Another question content',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_data_remains_untouched_after_foreign_put(self):
        self.client.force_authenticate(user=self.foreign_account)  
        response = self.client.put(reverse('questions:questions-detail', args=(self.question.id,)), {
            'summary': 'Another question heading',
            'content': 'Another question content',
        })
        question = Question.objects.get(pk=self.question.id)
        self.assertEqual(question.summary, 'Some title')
        self.assertEqual(question.content, 'Some text')

    def test_detail_returns_400_to_invalid_put(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.put(reverse('questions:questions-detail', args=(self.question.id,)), {
            'summary': 'Another question heading'*500,
            'content': 'Question content',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_data_remains_untouched_after_invalid_put(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.put(reverse('questions:questions-detail', args=(self.question.id,)), {
            'summary': 'Another question heading'*500,
            'content': 'Another question content',
        })
        question = Question.objects.get(pk=self.question.id,)
        self.assertEqual(question.summary, 'Some title')
        self.assertEqual(question.content, 'Some text')

    def test_detail_modifies_data_after_valid_post(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.put(reverse('questions:questions-detail', args=(self.question.id,)), {
            'summary': 'Another question heading',
            'content': 'Another question content',
        })
        question = Question.objects.get(pk=self.question.id,)
        self.assertEqual(question.summary, 'Another question heading')
        self.assertEqual(question.content, 'Another question content')

    def test_detail_returns_403_to_anon_delete(self):
        response = self.client.delete(reverse('questions:questions-detail', args=(self.question.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_data_remains_untouched_after_anon_delete(self):
        self.client.delete(reverse('questions:questions-detail', args=(self.question.id,)))
        self.assertEqual(Question.objects.count(), 1)

    def test_detail_returns_403_to_foreign_delete(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.delete(reverse('questions:questions-detail', args=(self.question.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_data_remains_untouched_after_foreign_delete(self):
        self.client.force_authenticate(user=self.foreign_account)
        self.client.delete(reverse('questions:questions-detail', args=(self.question.id,)))
        self.assertEqual(Question.objects.count(), 1)

    def test_detail_removes_instance_after_own_delete(self):
        self.client.force_authenticate(user=self.account)
        self.client.delete(reverse('questions:questions-detail', args=(self.question.id,)))
        self.assertEqual(Question.objects.count(), 0)

    def test_comment_it_returns_403_to_anon_user(self):
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'comment_it/',
            {
                'content': 'Some comment'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_it_returns_400_after_invalid_post(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'comment_it/',
            {
                'content': 'Some comment'*50
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_it_creates_comment_after_valid_post(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'comment_it/',
            {
                'content': 'Some comment'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.last().content, 'Some comment')

    def test_like_it_returns_403_to_anon_user(self):
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'like_it/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_it_creates_like_after_post(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'like_it/'
        )
        self.assertEqual(Like.objects.count(), 1)

    def test_dislike_it_returns_403_to_anon_user(self):
        response = self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'dislike_it/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dislike_it_removes_like_after_delete(self):
        like = Like.objects.create(
            content_object=self.question,
            author=self.foreign_account
        )
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'dislike_it/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)


class AnswerViewSetTest(APITestCase):

    def setUp(self):
        self.account = Account.objects.create_user(
            username='Andrew',
            email='pop@tut.by',
            password='homm1994'
        )
        self.foreign_account = Account.objects.create_user(
            username='Andri',
            email='popow@mail.ru',
            password='homm1994'
        )
        self.question = Question.objects.create(
            summary='Some title',
            content='Some text',
            author=self.account
        )
        self.answer = Answer.objects.create(
            content='Some answer',
            author=self.account,
            question=self.question
        )

    def test_list_returns_403_to_anon_user(self):
        response = self.client.get(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_returns_data_to_authed_user(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.get(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['content'], self.answer.content)

    def test_list_returns_403_to_anon_post(self):
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/',
            {'content': 'Some other answer'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_returns_400_after_invalid_post(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/',
            {'content': 'Some other answer'*500}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_data_remains_untouched_after_invalid_post(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/',
            {'content': 'Some other answer'*500}
        )
        self.assertEqual(Answer.objects.count(), 1)

    def test_list_modifies_data_after_valid_post(self):
        self.client.force_authenticate(user=self.account)
        self.client.force_authenticate(user=self.account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/',
            {'content': 'Some other answer'}
        )
        answer = Answer.objects.last()
        self.assertEqual(Answer.objects.count(), 2)
        self.assertEqual(answer.content, 'Some other answer')

    def test_detail_returns_403_to_anon_user_get(self):
        response = self.client.get(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_returns_data_to_authed_user_get(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.get(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], self.answer.content)

    def test_detail_returns_403_to_anon_put(self):
        response = self.client.put(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id,
            {'content': 'Some other answer'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_returns_403_to_foreign_put(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.put(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id,
            {'content': 'Some other answer'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_data_remains_untouched_after_foreign_put(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.put(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id,
            {'content': 'Some other answer'}
        )
        self.assertEqual(Answer.objects.first().content, self.answer.content)

    def test_detail_returns_400_after_invalid_put(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.put(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id,
            {'content': 'Some other answer'*500}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detail_data_remains_untouched_after_invalid_put(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.put(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id,
            {'content': 'Some other answer'*500}
        )
        self.assertEqual(Answer.objects.first().content, self.answer.content)

    def test_detail_modifies_data_after_valid_put(self):
        self.client.force_authenticate(user=self.account)
        response = self.client.put(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id,
            {'content': 'Some other answer'}
        )
        self.assertEqual(Answer.objects.first().content, 'Some other answer')

    def test_detail_returns_403_to_anon_delete(self):
        response = self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_data_remains_untouched_after_anon_delete(self):
        self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id
        )
        self.assertEqual(Answer.objects.count(), 1)

    def test_detail_returns_403_to_foreign_delete(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_data_remains_untouched_after_foreign_delete(self):
        self.client.force_authenticate(user=self.foreign_account)
        self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id
        )
        self.assertEqual(Answer.objects.count(), 1)

    def test_detail_removes_instace_after_own_delete(self):
        self.client.force_authenticate(user=self.account)
        self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id
        )
        self.assertEqual(Answer.objects.count(), 0)

    def test_comment_it_returns_403_to_anon_user(self):
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id + 'comment_it/',
            {
                'content': 'Some comment'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_it_returns_400_after_invalid_post(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id + 'comment_it/',
            {
                'content': 'Some comment'*500
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_it_creates_comment_after_valid_post(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id + 'comment_it/',
            {
                'content': 'Some comment'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.last().content, 'Some comment')

    def test_like_it_returns_403_to_anon_user(self):
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id + 'like_it/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like_it_creates_like_after_post(self):
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.post(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id + 'like_it/'
        )
        self.assertEqual(Like.objects.count(), 1)

    def test_dislike_it_returns_403_to_anon_user(self):
        response = self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id + 'dislike_it/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_dislike_it_removes_like_after_delete(self):
        like = Like.objects.create(
            content_object=self.answer,
            author=self.foreign_account
        )
        self.client.force_authenticate(user=self.foreign_account)
        response = self.client.delete(
            reverse('questions:questions-detail', args=(self.question.id,)) + 'answers/%d/' % self.answer.id + 'dislike_it/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

