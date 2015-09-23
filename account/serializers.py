from rest_framework import serializers
from questions.models import Answer, Question
from .models import Account


class ShortenedContentField(serializers.CharField):

	def to_representation(self, value):
		return value[:50]


class ForAccountQuestionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields = (
			'id',
			'summary',
			'comments_count',
			'answers_count',
			'likes_count',
		)


class ForAccountAnswerSerializer(serializers.ModelSerializer):
	content = ShortenedContentField()

	class Meta:
		model = Answer
		fields = (
			'id',
			'content',
			'comments_count',
			'likes_count',
			'solution',
		)


class AccountSerializer(serializers.ModelSerializer):
	own_questions = ForAccountQuestionSerializer(read_only=True, many=True)
	own_answers = ForAccountAnswerSerializer(read_only=True, many=True)

	class Meta:
		model = Account
		fields = (
			'id',
			'own_questions',
			'own_answers',
		)



class ForQuestionsAccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = (
			'id',
			'username',
			'email',
			'tagline',
			'description',
			'photo',
		)		