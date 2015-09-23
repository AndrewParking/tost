from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from .models import Question, Answer, Comment, Like, Tag
from .forms import AddQuestionForm
from .serializers import (
    QuestionSerializer,
    AnswerSerializer,
    NestedCommentSerializer,
    NestedLikeSerializer,
)
from .permissions import (
    IsAuthenticatedOrNotAllowed,
    IsOwnerOrReadOnly,
    IsOwnerOrQOwnerOrReadOnly,
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
        elif self.type == 'by_tag_id':
            tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
            data['title'] = 'Questions tagged with #%s' % tag.name
        return data


class PaginatedResponseMixin(object):

    def get_context_data(self, **kwargs):
        data = super(PaginatedResponseMixin, self).get_context_data(**kwargs)
        questions = data['questions']
        paginator = Paginator(questions, 6)
        # process exception
        page_num = self.request.GET.get('page', 1)
        data['questions'] = paginator.page(page_num)
        return data


# ============================================
# ================ Views =====================
# ============================================


class QuestionsListView(RedirectAnonUserMixin, SearchFieldMixin, PaginatedResponseMixin, ListView):
    template_name = 'questions/questions_list.html'
    context_object_name = 'questions'
    type = 'latest'

    def get_queryset(self):
        queryset = super(QuestionsListView, self).get_queryset()
        return queryset.order_by('-created_at')


class BestQuestionsListView(RedirectAnonUserMixin, SearchFieldMixin, PaginatedResponseMixin, ListView):
    template_name = 'questions/questions_list.html'
    context_object_name = 'questions'
    type = 'best'

    def get_queryset(self):
        queryset = super(BestQuestionsListView, self).get_queryset()
        # maybe performance bottleneck
        return sorted(queryset, key=lambda quest: quest.likes_count, reverse=True)


class UnansweredQuestionsListView(RedirectAnonUserMixin, SearchFieldMixin, PaginatedResponseMixin, ListView):
    template_name = 'questions/questions_list.html'
    context_object_name = 'questions'
    type = 'unanswered'

    def get_queryset(self):
        queryset = super(UnansweredQuestionsListView, self).get_queryset()
        # may also be performance bottleneck
        return [quest for quest in queryset if quest.answers_count == 0]


class ByTagIdQuestionsListView(RedirectAnonUserMixin, SearchFieldMixin, PaginatedResponseMixin, ListView):
    template_name = 'questions/questions_list.html'
    context_object_name = 'questions'
    type = 'by_tag_id'

    def get_queryset(self):
        queryset = super(ByTagIdQuestionsListView, self).get_queryset()
        tag = get_object_or_404(Tag, pk=self.kwargs['pk'])
        return queryset.filter(tags=tag)


class QuestionsDetailView(RedirectAnonUserMixin, DetailView):
    model = Question
    template_name = 'questions/questions_detail.html'
    context_object_name = 'question'

    def get_similar(self, tags, q_id, result=None):
        """
        Method to select similar to the gived one (q_id) questions.
        Algorithm filters questions in for-cycle by the inclusion of
        all the tags. If the quantity of questions is not enough (<4),
        one of the tags, which was included in the fewest number of questions
        is removed and method recursively calls itself.
        """
        temp_result = Question.objects.all()
        scores = {}
        for tag in tags:
            if scores.get(tag.name, False):
                scores[tag.name] += 1
            else:
                scores[tag.name] = 1
            temp_result = temp_result.filter(tags=tag)
        if result == None:
            fin_result = temp_result.exclude(pk=q_id)
        else:
            fin_result = result | temp_result.exclude(pk=q_id).distinct()
        fin_result = fin_result.distinct()
        if fin_result.count() >= 4:
            return fin_result[:4]
        elif len(tags) == 0:
            return fin_result
        else:
            min_val, min_name = Question.objects.count(), ''
            for name in scores:
                if min_val > scores[name]:
                    min_name, min_val = name, scores[name]
            tags = tags.exclude(name=min_name) 
            return self.get_similar(tags, q_id, result=fin_result)

    def get_context_data(self, **kwargs):
        data = super(QuestionsDetailView, self).get_context_data(**kwargs)
        match_list = []
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        tags = question.tags.all()
        data['similar'] = self.get_similar(tags, question.id)
        return data


class AddQuestionView(RedirectAnonUserMixin, FormView):
    form_class = AddQuestionForm
    template_name = 'questions/add_question.html'
    success_url = reverse_lazy('questions:questions_latest')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()
        form.save_m2m()
        return super(AddQuestionView, self).form_valid(form)


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
        serializer = QuestionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = QuestionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        if request.user != question.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = QuestionSerializer(question, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        if question.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def comment_it(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = NestedCommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(content_object=question, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def like_it(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        serializer = NestedLikeSerializer(data=request.data)
        if serializer.is_valid():
            for like in Like.objects.all():
                if like.author == request.user and like.content_object == question:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save(content_object=question, author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['delete'])
    def dislike_it(self, request, pk=None):
        question = get_object_or_404(Question, pk=pk)
        for like in Like.objects.all():
            if like.author == request.user and like.content_object == question:
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AnswersViewSet(ViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (
        IsAuthenticatedOrNotAllowed,
        IsOwnerOrQOwnerOrReadOnly,
    )

    def list(self, request, question_pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        queryset = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, question_pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        serializer = AnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(question=question, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        serializer = AnswerSerializer(answer, context={'request': request})
        return Response(serializer.data)

    def update(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        if request.user != answer.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = AnswerSerializer(answer, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        if request.user != answer.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'])
    def comment_it(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        serializer = NestedCommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(content_object=answer, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def like_it(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        serializer = NestedLikeSerializer(data=request.data)
        if serializer.is_valid():
            for like in Like.objects.all():
                if like.author == request.user and like.content_object == answer:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save(content_object=answer, author=request.user)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['delete'])
    def dislike_it(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        for like in Like.objects.all():
            if like.author == request.user and like.content_object == answer:
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route(methods=['patch'])
    def mark_as_solution(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        if question.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        answer.solution = True
        answer.save()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['patch'])
    def remove_solution_mark(self, request, question_pk=None, pk=None):
        question = get_object_or_404(Question, pk=question_pk)
        answer = get_object_or_404(Answer, question=question, pk=pk)
        if question.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        answer.solution = False
        answer.save()
        return Response(status=status.HTTP_200_OK)


class CommentsViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = NestedCommentSerializer
    permission_classes = (IsAuthenticatedOrNotAllowed, IsOwnerOrReadOnly)