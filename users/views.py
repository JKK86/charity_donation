from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import CreateView, FormView

from donation.models import Donation
from users.forms import RegistrationForm

User = get_user_model()


class UserRegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password1'],
            is_active=False,
        )
        # user = form.save(commit=False)
        # user.is_active = False
        # user.save()
        current_site = get_current_site(self.request)
        subject = "Aktywacja konta"
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'protocol': 'http',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data['email']
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.send()
        # messages.success(self.request, "Użytkownik został pomyślnie zarejestrowany")
        return HttpResponse('Potwierdź swój adres e-mail, aby zakończyć rejestrację.')


class UserProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user)
        return render(request, 'user_profile.html', {'donations': donations})


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(self.request, "Konto zostało aktywowane")
            return redirect('login')
        else:
            messages.error(self.request, "Link aktywacyjny jest nieprawidłowy")
            return redirect('register')


class EditProfile(View):
    pass