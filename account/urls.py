from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='profile'),
    url(r'^update_account/$', views.UpdateAccountView.as_view(), name='update_account'),
    url(r'^sign-up/$', views.SignUpView.as_view(), name='sign_up'),
    url(r'^sign-in/$', views.SignInView.as_view(), name='sign_in'),
]