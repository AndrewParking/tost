from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import smart_text
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.viewsets import ModelViewSet
from .forms import CreateAccountForm, UpdateAccountForm
from .serializers import AccountSerializer
from .permissions import IsAuthenticatedOrNotAllowed, IsOwnerOrReadOnly
from .tasks import send_login_email, send_account_change_email, send_verification_email
from .models import Account

# Create your views here.

# =======================================================
# ======================= Mixins ========================
# =======================================================


class RedirectAnonUserMixin(object):

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('account:sign_in'))
        return super(RedirectAnonUserMixin, self).dispatch(*args, **kwargs)


class RedirectAuthedUserMixin(object):

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('account:profile', args=(user.id,)))
        return super(RedirectAuthedUserMixin, self).dispatch(*args, **kwargs)


# =======================================================
# ======================= Views =========================
# =======================================================


class ProfileView(RedirectAnonUserMixin, DetailView):
    model = Account
    template_name = 'account/profile.html'
    context_object_name = 'account'


class SignUpView(RedirectAuthedUserMixin, FormView):
    template_name = 'account/sign_up.html'
    form_class = CreateAccountForm

    def get_success_url(self):
        return reverse_lazy('account:profile', args=(self.request.user.id,))

    def get_form_kwargs(self):
        kwargs = super(SignUpView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.clean_password2()
        form.save()
        form.login_user()
        send_verification_email.delay(self.request.user.id,)
        return super(SignUpView, self).form_valid(form)


class SignInView(RedirectAuthedUserMixin, FormView):
    template_name = 'account/sign_in.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('account:profile', args=(self.request.user.id,))

    def form_valid(self, form):
        user = form.get_user()
        form.confirm_login_allowed(user)
        login(self.request, user)
        send_login_email.delay(self.request.user.id,)
        return super(SignInView, self).form_valid(form)


class UpdateAccountView(RedirectAnonUserMixin, FormView):
    template_name = 'account/update_account.html'
    form_class = UpdateAccountForm

    def get_success_url(self):
        return reverse_lazy('account:profile', args=(self.request.user.id,))

    def get_form_kwargs(self):
        kwargs = super(UpdateAccountView, self).get_form_kwargs()
        kwargs['instance'] = Account.objects.get(pk=self.request.user.id)
        return kwargs

    def get_changes(self, form):
        changes = {}
        account = Account.objects.get(pk=self.request.user.id).__dict__
        for key in form.cleaned_data:
            if form.cleaned_data.get(key) != account.get(key):
                if key == 'password': continue
                changes[key] = form.cleaned_data[key]
        return changes

    def form_valid(self, form):
        changes = self.get_changes(form)
        form.save()
        send_account_change_email.delay(self.request.user.id, changes)
        return super(UpdateAccountView, self).form_valid(form)


class LogOutView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return reverse_lazy('account:sign_in')


class VerificationView(View):

    def get(self, request):
        link = request.GET.get('link')
        if link:
            account = Account.objects.get(pk=request.user.id)
            account_link = account.link
            if account_link.value == link:
                account.verified = True
                account_link.delete()
                account.save()
        return HttpResponseRedirect(reverse_lazy('account:profile', args=(account.id,)))


# =====================================================
# ==================== API Views ======================
# =====================================================


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
        IsAuthenticatedOrNotAllowed,
    )
