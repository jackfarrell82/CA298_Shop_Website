from django.contrib import admin
from django.urls import path, include
from jackshop import views
from django.conf import settings
from django.conf.urls.static import static 
from .forms import UserSignupForm, UserLoginForm

urlpatterns = [
    path('', views.index, name='homepage'),
    path('products/<int:prodid>', views.product_individual, name="individual_product"),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
    path('logout/', views.logout_user, name="logout"),
    path('addbasket/<int:prodid>', views.add_to_basket, name="add_basket"),
    path('products/', views.products, name="products"),
    path('basket/', views.show_basket, name="show_basket"),
    path('removeitem/<int:sbi>', views.remove_item, name="remove_item"),
    path('order/', views.order, name="order")
]