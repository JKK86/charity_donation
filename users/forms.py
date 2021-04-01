from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm, \
    SetPasswordForm

from django import forms
from django.core.exceptions import ValidationError

User = get_user_model()


class RegistrationForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
            attrs={'placeholder': 'Powtórz hasło'}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email',]
        field_classes = {}
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }


class UserLoginForm(AuthenticationForm):
    username = None
    email = UsernameField(widget=forms.EmailInput(
        attrs={'autofocus': True,'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Hasło'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        self.username_field = get_user_model()._meta.get_field(get_user_model().USERNAME_FIELD)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.username_field.verbose_name},
        )

    error_messages = {
        'invalid_login': (
            "Podaj prawidłowy adres email i hasło"
        ),
        'inactive': ("Konto jest nieaktywne."),
    }


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=64,
                             label='',
                             widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'Email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Podany adres email nie występuje w naszej bazie')
        return email


class SetNewPassword(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Nowe hasło'}),
        strip=False,
        label=""
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Powtórz hasło'}),
        strip=False,
        label=""
    )