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


class Question(TimeStampMixin):
    summary = models.CharField(blank=False, max_length=250)
    content = models.TextField(blank=False)
    author = models.ForeignKey(Account, related_name='questions')
    comments = GenericRelation('Comment')
    likes = GenericRelation('Like')

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.summary


class Answer(TimeStampMixin):
    content = models.TextField()
    question = models.ForeignKey(Question, related_name='question_answers')
    author = models.ForeignKey(Account, related_name='author_answers')
    comments = GenericRelation('Comment')
    likes = GenericRelation('Like')

    @property
    def comments_count(self):
        return self.comments.count()

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.content[:30]


class Comment(TimeStampMixin):
    content = models.TextField(max_length=400)
    author = models.ForeignKey(Account, related_name='comments')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content[:30]


class Like(TimeStampMixin):
    author = models.ForeignKey(Account)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '%s: %s' % (self.author.username, self.created_at)