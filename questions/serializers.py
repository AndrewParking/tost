from rest_framework import serializers
from account.serializers import ForQuestionsAccountSerializer
from .models import Question, Answer, Comment, Like, Tag


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


class NestedTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class NestedLikeSerializer(serializers.ModelSerializer):
    content_object = ContentTypeRelatedField(read_only=True)
    author = ForQuestionsAccountSerializer(read_only=True)

    class Meta:
        model = Like
        fields = (
            'id',
            'author',
            'content_object',
        )


class NestedCommentSerializer(serializers.ModelSerializer):
    content_object = ContentTypeRelatedField(read_only=True)
    author = ForQuestionsAccountSerializer(read_only=True)
    my = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'content',
            'author',
            'content_object',
            'my',
        )

    def get_my(self, obj):
        if obj.author == self.context['request'].user:
            return True
        return False


class AnswerSerializer(serializers.ModelSerializer):
    author = ForQuestionsAccountSerializer(read_only=True)
    comments = NestedCommentSerializer(many=True, read_only=True)
    already_liked = serializers.SerializerMethodField()
    my = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = (
            'id',
            'content',
            'author',
            'comments',
            'likes_count',
            'already_liked',
            'my',
            'solution',
        )

    def get_already_liked(self, obj):
        for like in Like.objects.all():
            if like.author == self.context['request'].user and like.content_object == obj:
                return True
        return False

    def get_my(self, obj):
        if obj.author == self.context['request'].user:
            return True
        return False


class QuestionSerializer(serializers.ModelSerializer):
    author = ForQuestionsAccountSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    tags = NestedTagSerializer(many=True, read_only=True)
    comments = NestedCommentSerializer(many=True, read_only=True)
    already_liked = serializers.SerializerMethodField()
    my = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'summary',
            'content',
            'tags',
            'author',
            'answers',
            'comments',
            'likes_count',
            'already_liked',
            'my',
        )

    def get_already_liked(self, obj):
        for like in Like.objects.all():
            if like.author == self.context['request'].user and like.content_object == obj:
                return True
        return False

    def get_my(self, obj):
        if obj.author == self.context['request'].user:
            return True
        return False