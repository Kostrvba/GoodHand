from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from GoodHands.models import Donation, Institution, User, Category
from django.conf import settings


class LandingPage(View):

    def get(self, request):
        donations = Donation.objects.all().count()
        organisations = Institution.objects.all().count()
        foundations = Institution.objects.filter(type=Institution.FUNDACJA)
        organs = Institution.objects.filter(type=Institution.ORGANIZACJA_POZARZADOWA)
        locals = Institution.objects.filter(type=Institution.ZBIORKA_LOKALNA)
        return render(request, 'index.html',
                      {'donations': donations, 'organisations': organisations, 'foundations': foundations,
                       'organs': organs, 'locals': locals})


class AddDonation(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('main')
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        selected_categories = ','.join(str(cat.pk) for cat in categories)
        context = {
            'categories': categories,
            'institutions': institutions,
            'selected_categories': selected_categories,
        }
        return render(request, 'form.html', context)



class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        return redirect('register')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create_user(username=email, email=email)
            user.set_password(password)
            user.first_name = name
            user.last_name = surname
            user.save()
            return redirect('login')
        return render(request, 'register.html')


class Account(View):
    @method_decorator(login_required)
    def get(self, request):
        user_id = request.user.id
        donations = Donation.objects.filter(user_id=user_id)
        return render(request, 'user.html', {'donations': donations})


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
