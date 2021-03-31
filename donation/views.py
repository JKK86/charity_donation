from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.views import View

from donation.models import Donation, Institution, FUNDACJA, ORG_POZA, ZB_LOK, Category

User = get_user_model()


class LandingPageView(View):
    def get(self, request):
        quantity = sum([donation.quantity for donation in Donation.objects.all()])
        donated_institutions = Institution.objects.filter(donations__isnull=False).distinct().count()
        # institutions = Institution.objects.all().count() - Institution.objects.filter(donation__isnull=True).count()
        institutions = Institution.objects.all()
        foundations_list = institutions.filter(type=FUNDACJA)
        organizations_list = institutions.filter(type=ORG_POZA)
        collections_list = institutions.filter(type=ZB_LOK)
        paginator_f = Paginator(foundations_list, 2)
        page = request.GET.get('page', 1)
        try:
            foundations = paginator_f.page(page)
        except PageNotAnInteger:
            foundations = paginator_f.page(1)
        except EmptyPage:
            foundations = paginator_f.page(paginator_f.num_pages)

        paginator_o = Paginator(organizations_list, 2)
        page = request.GET.get('page', 1)
        try:
            organizations = paginator_o.page(page)
        except PageNotAnInteger:
            organizations = paginator_o.page(1)
        except EmptyPage:
            organizations = paginator_o.page(paginator_f.num_pages)

        paginator_c = Paginator(collections_list, 2)
        page = request.GET.get('page', 1)
        try:
            collections = paginator_c.page(page)
        except PageNotAnInteger:
            collections = paginator_c.page(1)
        except EmptyPage:
            collections = paginator_c.page(paginator_f.num_pages)
        return render(request, 'index.html', {
            'quantity': quantity,
            'donated_institutions': donated_institutions,
            'foundations': foundations,
            'organizations': organizations,
            'collections': collections
        })


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})

    def post(self, request):
        user = request.user
        organization_id=request.POST['organization']
        organization = Institution.objects.get(pk=organization_id)
        donation = Donation.objects.create(
            quantity=request.POST['bags'],
            institution=organization,
            address=request.POST['address'],
            phone_number=request.POST['phone'],
            city=request.POST['city'],
            zip_code=request.POST['postcode'],
            pick_up_date=request.POST['data'],
            pick_up_time=request.POST['time'],
            pick_up_comment=request.POST['more_info'],
            user=user,
        )
        category_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=category_ids)
        donation.categories.set(categories)
        donation.save()
        return render(request, 'form-confirmation.html')


# class LoginView(View):
#     def get(self, request):
#         return render(request, 'registration/login.html')
#
#     def post(self, request):
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(email=email, password=password)
#         if user:
#             login(request, user)
#             return redirect('start')
#         else:
#             messages.error(request, "Użytkownik nie został znaleziony. Zarejestruj się w serwisie i spróbuj ponownie")
#             return redirect('register')


# class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return redirect('start')


# class RegisterView(View):
#     def get(self, request):
#         return render(request, 'registration/register.html')
#
#     def post(self, request):
#         User.objects.create_user(
#             email=request.POST['email'],
#             first_name=request.POST['name'],
#             last_name=request.POST['surname'],
#             password=request.POST['password']
#         )
#         return redirect('login')