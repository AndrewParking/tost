from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CreateAccountForm, UpdateAccountForm
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

    def form_valid(self, form):
        form.save()
        return super(UpdateAccountView, self).form_valid(form)
