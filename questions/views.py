from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from .models import Question, Answer, Comment, Like
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    NestedCommentSerializer,
    NestedLikeSerializer,
)
from .permissions import (
    IsAuthenticatedOrNotAllowed,
    IsOwnerOrReadOnly,
)

# Create your views here.


# ============================================
# =============== Mixins =====================
# ============================================


class RedirectAnonUserMixin(object):

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('account:sign_in'))
        return super(RedirectAnonUserMixin, self).dispatch(*args, **kwargs)


class SearchFieldMixin(object):

    def get_queryset(self):
        if self.request.GET.get('q'):
            q = self.request.GET['q']
            return Question.objects.filter(Q(summary__icontains=q) | Q(content__icontains=q))
        else:
            return Question.objects.all()

    def get_context_data(self, **kwargs):
        data = super(SearchFieldMixin, self).get_context_data(**kwargs)
        if self.request.GET.get('q'):
            q = self.request.GET['q']
            data['search_results'] = 'This is search results for \'%s\' query.' % q
        data['type'] = self.type
        if self.type == 'latest':
            data['title'] = 'Latest questions'
        elif self.type == 'best':
            data['title'] = 'Best questions'
        elif self.type == 'unanswered':
            data['title'] = 'Questions without answer'
        return data


# ============================================
# ================ Views =====================
# ============================================


class QuestionsListView(RedirectAnonUserMixin, SearchFieldMixin, ListView):
    template_name = 'questions/questions_list.html'
    context_object_name = 'questions'
    type = 'latest'

    def get_queryset(self):
        queryset = super(QuestionsListView, self).get_queryset()
        return queryset.order_by('-created_at')


class BestQuestionsListView(RedirectAnonUserMixin, SearchFieldMixin, ListView):
    template_name = 'questions/questions_list.html'
    context_object_name = 'questions'
    type = 'best'

    def get_queryset(self):
        queryset = super(BestQuestionsListView, self).get_queryset()
        # maybe performance bottleneck
        return sorted(queryset, key=lambda quest: quest.likes_count, reverse=True)


class UnansweredQuestionsListView(RedirectAnonUserMixin, SearchFieldMixin, ListView):
    template_name = 'questions/questions_list.html'
    context_object_name = 'questions'
    type = 'unanswered'

    def get_queryset(self):
        queryset = super(UnansweredQuestionsListView, self).get_queryset()
        # may also be performance bottleneck
        return [quest for quest in queryset if quest.answers_count == 0]


# =========================================================
# ======================= API Views =======================
# =========================================================


class QuestionsViewSet(ViewSet):
    serializer_class = QuestionSerializer
    permission_classes = (
        IsAuthenticatedOrNotAllowed,
        IsOwnerOrReadOnly,
    )

    def list(self, request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def update(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def comment_it(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = NestedCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content_object=question, author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def like_it(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = NestedLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content_object=question, author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswersViewSet(ViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (
        IsAuthenticatedOrNotAllowed,
        IsOwnerOrReadOnly,
    )

    def list(self, request, question_pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        queryset = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, question_pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

    def update(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        serializer = AnswerSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def comment_it(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        serializer = NestedCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content_object=answer, author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_201_CREATED)

    @detail_route(methods=['post'])
    def like_it(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        serializer = NestedLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(content_object=answer, author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_201_CREATED)
