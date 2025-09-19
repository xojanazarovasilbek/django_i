from django.shortcuts import render, redirect
from .models import Transaction, Category, Card
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm, CategoryForm, CardForm, ProfilForm
from datetime import date, timedelta
from django.utils.timezone import now
from django.db.models import Sum
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  
            category.save()
            return redirect("categories") 
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, "categories.html", {"categories": categories})


@login_required
def dashboard(request):
    today = date.today()
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')

    period = request.GET.get("period", "all")

    if period == "day":
        transactions = transactions.filter(created_at__date=today)
    elif period == "week":
        start_week = today - timedelta(days=today.weekday())
        transactions = transactions.filter(created_at__date__gte=start_week)
    elif period == "month":
        transactions = transactions.filter(created_at__year=today.year, created_at__month=today.month)
    elif period == "year":
        transactions = transactions.filter(created_at__year=today.year)

    total_income = transactions.filter(type="income").aggregate(Sum("amount"))["amount__sum"] or 0
    total_expense = transactions.filter(type="expense").aggregate(Sum("amount"))["amount__sum"] or 0

    cards = Card.objects.filter(user=request.user)
    cards_total = cards.aggregate(Sum("balance"))["balance__sum"] or 0

    balance = total_income - total_expense + cards_total
    balance_usd = round(balance / 12500, 2)  

    return render(request, "dashboard.html", {
        "transactions": transactions,
        "balance": balance,
        "balance_usd": balance_usd,
        "total_income": total_income,
        "total_expense": total_expense,
        "period": period,
        "cards": cards,
        "income": total_income,
        "expense": total_expense,
    })



def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user

            card_id = request.POST.get('card')
            if card_id:
                card = Card.objects.get(id=card_id)

                if transaction.type == 'chiqim':
                    card.balance -= transaction.amount
                elif transaction.type == 'kirim':  
                    card.balance += transaction.amount

                card.save()
                transaction.card = card  

            transaction.save()
            return redirect('transactions')
    else:
        form = TransactionForm()

    cards = Card.objects.filter(user=request.user)
    return render(request, 'transaction_form.html', {'form': form, 'cards': cards})

def Kirim(request):
    transactions = Transaction.objects.filter(user=request.user, type='income')
    return render(request, 'kirim.html', {'transactions': transactions})

def Chiqim(request):
    transactions = Transaction.objects.filter(user=request.user, type='expense')
    return render(request, 'chiqim.html', {'transactions': transactions})




def add_card(request):
    if request.method == "POST":
        name = request.POST.get("name")
        number = request.POST.get("number")
        balance = request.POST.get("balance")
        currency = request.POST.get("currency")

        try:
            Card.objects.create(
                user=request.user,
                name=name,
                number=number,
                balance=balance,
                currency=currency
            )
            messages.success(request, "Karta muvaffaqiyatli qo‘shildi!")
            return redirect("dashboard")
        except IntegrityError:
            messages.error(request, "Bu karta raqami allaqachon mavjud.")
            return redirect("add_card")

    return render(request, "add_card.html")




@login_required(login_url = 'login')
def profile(resquest):
    user = User.objects.get(username=resquest.user.username)
    return render(resquest, 'profile.html', {'user':user})

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil muvaffaqiyatli yangilandi!")
            return redirect('profile') 
    else:
        form = ProfilForm(instance=request.user)

    return render(request, 'profile_update.html', {'form': form})

