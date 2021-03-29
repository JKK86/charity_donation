from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView

from users.forms import RegistrationForm

User = get_user_model()


class UserRegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        User.objects.create_user(
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password1'],
        )
        messages.success(self.request, "Użytkownik został pomyślnie zarejestrowany")
        return super().form_valid(form)
