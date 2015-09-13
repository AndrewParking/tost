from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^sign-up/$', views.SignUpView.as_view(), name='sign_up'),
]