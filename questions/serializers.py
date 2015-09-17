from rest_framework import serializers
from .models import Question, Answer, Comment, Like


class ContentTypeRelatedField(serializers.RelatedField):
    """
    Custom fiels to user for content_object fields representation
    """

    def to_representation(self, value):
        """
        Serialize content_object to a simple textual representation
        """
        if isinstance(value, Question):
            return 'Question: %s' % value.id
        elif isinstance(value, Answer):
            return 'Answer: %s' % value.id
        else:
            raise Exception('Unexpected type of tagged object')


class NestedLikeSerializer(serializers.ModelSerializer):
    content_object = ContentTypeRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = (
            'author',
            'content_object',
        )


class NestedCommentSerializer(serializers.ModelSerializer):
    content_object = ContentTypeRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'content',
            'author',
            'content_object',
        )


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = NestedCommentSerializer(many=True, read_only=True)
    likes = NestedLikeSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = (
            'content',
            'author',
            'comments',
            'likes',
        )


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    comments = NestedCommentSerializer(many=True, read_only=True)
    likes = NestedLikeSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'summary',
            'content',
            'author',
            'answers',
            'comments',
            'likes',
        )