from django.test import TestCase
from .forms import AddQuestionForm
from .models import Tag


class AddFormTestCase(TestCase):

	def test_with_empty_data(self):
		form = AddQuestionForm({})
		self.assertFalse(form.is_valid())

	def test_with_invalid_data(self):
		tag = Tag.objects.create(name='test_tag')
		form = AddQuestionForm({
			'summary': 'A'*500,
			'content': 'Some content',
			'tags': [tag.id],
		})
		self.assertFalse(form.is_valid())

	def test_with_valid_data(self):
		tag = Tag.objects.create(name='test_tag')
		form = AddQuestionForm({
			'summary': 'Some summary',
			'content': 'Some content',
			'tags': [tag.id],
		})
		self.assertTrue(form.is_valid())