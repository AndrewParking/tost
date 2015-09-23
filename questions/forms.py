from django.forms import ModelForm
from .models import Question


class AddQuestionForm(ModelForm):

	class Meta:
		model = Question
		fields = (
			'summary',
			'content',
			'tags',
		)
		help_texts = {
			'summary': 'Tell the issue of the question in a few words',
			'content': 'Give full description of the problem',
			'tags': 'Choose some tags for users to find your question easily',
		}