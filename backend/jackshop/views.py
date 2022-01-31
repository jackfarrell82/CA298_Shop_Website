from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

def index(request):
    # get the request in
    # do some logic with models from the databasse
    # return some webpage to the user

    return render(request, "index.html", {'products': products})

def products(request):

    products = Product.objects.all()

    return render(request, "products.html", {'products': products})

def product_individual(request, prodid):
    # get the products with id = prodid
    product = Product.objects.get(id=prodid)
    return render(request, "product_individual.html", {'product':product})

class UserSignupView(CreateView):
    model = APIUser
    form_class = UserSignupForm
    template_name = 'user_register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('')

class UserLoginView(LoginView):
    template_name='login.html'

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def add_to_basket(request, prodid):
    user = request.user
    # is there a shopping basket for the user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if not basket:
        # create a new one
        basket = Basket(user_id=user).save()
    # get the product
    product = Product.objects.get(id=prodid)
    sbi = BasketItems.objects.filter(basket_id=basket, product_id=product).first()
    if sbi is None:
        # there is no basket item for that products
        # create one
        sbi = BasketItems(basket_id=basket, product_id=product).save()
    else:
        # a basket item already exists
        # just add 1 to the quantity
        sbi.quantity = sbi.quantity+1
        sbi.save()
    return render(request, 'product_individual.html', {'product':product, 'added':True})