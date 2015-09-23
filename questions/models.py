from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from account.models import Account

# Create your models here.

# ================================================
# =================== Mixins =====================
# ================================================


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ================================================
# =================== Models =====================
# ================================================


class Tag(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Question(TimeStampMixin):
    summary = models.CharField(max_length=250)
    content = models.TextField()
    author = models.ForeignKey(Account, related_name='own_questions', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='questions')
    comments = GenericRelation('Comment')
    likes = GenericRelation('Like')

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def answers_count(self):
        return self.answers.count()

    def __str__(self):
        return self.summary


class Answer(TimeStampMixin):
    content = models.CharField(max_length=1000)
    question = models.ForeignKey(Question, related_name='answers')
    author = models.ForeignKey(Account, related_name='own_answers', blank=True, null=True)
    comments = GenericRelation('Comment')
    likes = GenericRelation('Like')
    solution = models.BooleanField(default=False)

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.content[:30]


class Comment(TimeStampMixin):
    content = models.CharField(max_length=400)
    author = models.ForeignKey(Account, related_name='comments')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content[:30]


class Like(TimeStampMixin):
    author = models.ForeignKey(Account, related_name='likes')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '%s: %s' % (self.author.username, self.created_at)
