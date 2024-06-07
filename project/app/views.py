from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product, Category, News
from django.contrib.auth import login, logout
from .forms import LoginForm, RegisterForm
from .utils import CartAuthenticatedUser
from django.http import HttpResponse, HttpRequest
import stripe
from project import settings
# Create your views here.

def index(request):
    products = Product.objects.all
    categories = Category.objects.all
    news = News.objects.all
    context = {
        'products':products,
        'categories':categories,
        'news':news
    }
    return render(request, 'app/index.html', context)


def detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'app/product_detail.html', context)



def all_products(request):
    products = Product.objects.all
    categories = Category.objects.all
    context = {
        'products':products,
        'categories':categories
    }
    return render(request, 'app/all_products.html', context)




def to_cart(request: HttpRequest, product_id, action):
    if request.user.is_authenticated:
        CartAuthenticatedUser(request, product_id, action)
        current_page = request.META.get("HTTP_REFERER", 'index')
        return redirect(current_page)

    return redirect('login')


def all_news(request):
    news = News.objects.all
    context = {
        'news':news
    }
    return render(request,'app/news.html', context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    return render(request, 'app/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def user_register(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('index')
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'app/register.html', context)


def cart(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request)
        context = {
            'order_products': cart_info.get_cart_info()['order_products']
        }
        return render(request, 'app/cart.html', context)
    return redirect('login')


def create_chekout_sessions(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Product mahsulotlari'
                },
                'unit_amount': int(total_price * 300)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)



def success_payment(request):
    return render(request, 'app/success.html')

