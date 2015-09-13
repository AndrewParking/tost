from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account


class CreateAccountForm(UserCreationForm):

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