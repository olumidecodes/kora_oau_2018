from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
BankChoices = (
    ('Access Bank', 'Access Bank'),
    ('ALAT by Wema', 'ALAT by Wema'),
    ('Diamond Bank', 'Diamond Bank'),
    ('Fidelity Bank', 'Fidelity Bank'),
    ('FCMB', 'FCMB'),
    ('Sterling', 'Sterling'),
    ('Zenith', 'Zenith')
)

BankCodes = {
    'Access':'044',
    'ALAT by Wema': '035A',
    'Diamond': '063',
    'Fidelity Bank': '070',
    'FCMB': '214',
    'Sterling':'232',
    'Zenith': '057'


}

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')


class ReceivePaymentForm(forms.Form):
    recipient_name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    account_number = forms.CharField(max_length=10)
    bank = forms.CharField(max_length=20)