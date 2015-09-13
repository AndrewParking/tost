from django.contrib.auth.forms import UserCreationForm
from .models import Account


class CreateAccountForm(UserCreationForm):

    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'tagline',
            'description',
        )