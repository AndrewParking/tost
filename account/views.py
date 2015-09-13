from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from .forms import CreateAccountForm

# Create your views here.

# =======================================================
# ======================= Mixins ========================
# =======================================================


class RedirectAuthedUserMixin(object):

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated():
            return HttpResponseRedirect('/')  # TODO: replace the url of user's home page
        return super(RedirectAuthedUserMixin, self).dispatch(*args, **kwargs)


# =======================================================
# ======================= Views =========================
# =======================================================


class SignUpView(RedirectAuthedUserMixin, FormView):
    template_name = 'account/sign_up.html'
    form_class = CreateAccountForm
    success_url = '/'  # TODO: replace it with actual url of the user's home page

    def get_form_kwargs(self):
        kwargs = super(SignUpView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.clean_password2()
        form.save()
        form.login_user()
        return super(SignUpView, self).form_valid(form)
