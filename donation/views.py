from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
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
        paginator_f = Paginator(foundations_list, 5)
        page = request.GET.get('page', 1)
        try:
            foundations = paginator_f.page(page)
        except PageNotAnInteger:
            foundations = paginator_f.page(1)
        except EmptyPage:
            foundations = paginator_f.page(paginator_f.num_pages)

        paginator_o = Paginator(organizations_list, 5)
        page = request.GET.get('page', 1)
        try:
            organizations = paginator_o.page(page)
        except PageNotAnInteger:
            organizations = paginator_o.page(1)
        except EmptyPage:
            organizations = paginator_o.page(paginator_f.num_pages)

        paginator_c = Paginator(collections_list, 5)
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
        organization_id = request.POST['organization']
        organization = Institution.objects.get(pk=organization_id)
        quantity = request.POST['bags']
        address = request.POST['address']
        phone_number = request.POST['phone']
        city = request.POST['city']
        zip_code = request.POST['postcode']
        pick_up_date = request.POST['data']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST['more_info']
        donation = Donation.objects.create(
            quantity=quantity,
            institution=organization,
            address=address,
            phone_number=phone_number,
            city=city,
            zip_code=zip_code,
            pick_up_date=pick_up_date,
            pick_up_time=pick_up_time,
            pick_up_comment=pick_up_comment,
            user=user,
        )
        category_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(id__in=category_ids)
        donation.categories.set(categories)
        donation.save()

        subject = 'Potwierdzenie przekazania darowizny'
        message = render_to_string('donation_form_confirmation_email.html', {
            'user': user,
            'quantity': quantity,
            'organization': organization,
            'address': address,
            'zip_code': zip_code,
            'city': city,
            'pick_up_date': pick_up_date,
            'pick_up_time': pick_up_time
        })
        email_from = 'donation@local.com'
        email_to = [user.email]
        send_mail(subject, message, email_from, email_to, fail_silently=False)
        return render(request, 'form-confirmation.html')


class ArchiveDonationView(View):
    def post(self, request, donation_id):
        user = request.user
        donation = Donation.objects.get(pk=donation_id)
        donation.is_taken = True
        donation.save()
        return redirect('user_profile')


class ContactView(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        message = request.POST.get('message')
        subject = f'Wiadomosc od uzytkownika {name} {surname}'
        users = User.objects.filter(is_staff=True)
        email_from = 'donation@local.com'
        email_to = [user.email for user in users]
        # mail_admins (for sending an email to the site admins, as defined in the ADMINS setting.)
        send_mail(subject, message, email_from, email_to, fail_silently=False)
        return render(request, 'email_confirmation.html')

