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
        return redirect('/')

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
    if basket is None:
        # create a new one
        Basket.objects.create(user_id=user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
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


@login_required
def show_basket(request):
    # get user object
    # does a basket exist? -> your basket is empty
    # load all shopping basket items
    # display them on the page
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return render(request, 'basket.html', {'empty':True})
    else:
        sbi = BasketItems.objects.filter(basket_id=basket)
        # is the list empty?
        if sbi.exists():
            # normal flow
            return render(request, 'basket.html', {'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'basket.html', {'empty':True})

@login_required
def remove_item(request, sbi):
    basketitem = BasketItems.objects.get(id=sbi)
    if basketitem is None:
        return redirect('/basket') # if error - redirect to shopping basket
    else:
        if basketitem.quantity > 1:
            basketitem.quantity = basketitem.quantity-1
            basketitem.save() # save our changes in the data base
        else:
            basketitem.delete() # delete the basket item
    return redirect('/basket')

@login_required
def order(request):
    # load in all the data
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    if basket is None:
        return redirect('/')
    sbi = BasketItems.objects.filter(basket_id=basket)
    if not sbi.exists():
        return redirect('/')
    # are we dealing with a POST or GET request
    if request.method == "POST":
        # check form is valid
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.basket_id = basket
            total = 0.0
            for item in sbi:
                total += float(item.price())
            order.total_price = total
            order.save()
            basket.is_active = False
            basket.save()
            return render(request, 'ordercomplete.html', {'order':order, 'basket':basket, 'sbi':sbi})
        else:
            return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})  
    else:
        # show the form
        form = OrderForm()
        return render(request, 'orderform.html', {'form':form, 'basket':basket, 'sbi':sbi})