from django.shortcuts import render
from django.views import View

from donation.models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        quantity = sum([donation.quantity for donation in Donation.objects.all()])
        # institutions = Institution.objects.filter(donation__isnull=False).count()
        institutions = Institution.objects.all().count() - Institution.objects.filter(donation__isnull=True).count()
        return render(request, 'index.html', {'quantity': quantity, 'institutions': institutions})


class AddDonationView(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
