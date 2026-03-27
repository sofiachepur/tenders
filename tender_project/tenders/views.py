from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db import models
from django.core.mail import send_mail



# ✅ РЕЄСТРАЦІЯ
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')

        # перевірка чи існує користувач
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Користувач вже існує'})

        # створення користувача
        user = User.objects.create_user(username=username, password=password, email=email )

        # створення компанії
        Company.objects.create(
            user=user,
            name=company_name

        )

        return redirect('login')

    return render(request, 'register.html')


# ✅ ЛОГІН
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('tender_list')  # головна сторінка
        else:
            return render(request, 'login.html', {'error': 'Невірний логін або пароль'})

    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tender, Company, Proposal

@login_required(login_url='/login/')
def apply_tender(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)


    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        messages.warning(request, "У вас ще не створена компанія. Будь ласка, зареєструйте компанію перед подачею тендеру.")
        return redirect('/register/')

    if request.method == "POST":
        price = request.POST.get('price')
        if not price:
            messages.error(request, "Вкажіть ціну пропозиції.")
            return redirect('apply_tender', tender_id=tender.id)

        # створення пропозиції
        Proposal.objects.create(
            tender=tender,
            company=company,
            price=price
        )
        messages.success(request, "Ваша пропозиція успішно надіслана!")
        return redirect('tender_list')  # або на сторінку тендерів

    return render(request, 'apply.html', {'tender': tender})

from django.shortcuts import render
from .models import Tender

def tender_list(request):
    tenders = Tender.objects.all()
    return render(request, 'tenders.html', {'tenders': tenders})