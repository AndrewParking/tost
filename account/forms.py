from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login
from .models import Account


class CreateAccountForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        if kwargs.get('request'):
            self.request = kwargs.pop('request')
        super(CreateAccountForm, self).__init__(*args, **kwargs)

    def login_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        user = authenticate(
            username=username,
            password=password
        )
        login(self.request, user)

    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'photo',
            'tagline',
            'description',
        )


class UpdateAccountForm(UserChangeForm):

    def clean_password(self):
        return self.initial.get('password')

    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'photo',
            'tagline',
            'description',
        )