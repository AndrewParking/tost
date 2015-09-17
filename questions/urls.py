from django.conf.urls import url
from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter
from . import views


urlpatterns = [
    url(r'^$', views.QuestionsListView.as_view(), name='questions_latest'),
    url(r'^best/$', views.BestQuestionsListView.as_view(), name='questions_best'),
    url(r'^unanswered/$', views.UnansweredQuestionsListView.as_view(), name='questions_unanswered'),
]

router = routers.SimpleRouter()
router.register(r'questions', views.QuestionsViewSet, base_name='questions')

answers_router = NestedSimpleRouter(router, r'questions', lookup='question')
answers_router.register(r'answers', views.AnswersViewSet, base_name='answers')


urlpatterns += router.urls
urlpatterns += answers_router.urls