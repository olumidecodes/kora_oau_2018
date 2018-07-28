from django.urls import path, include
from home import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('', views.index, name='home'),
    path('<str:reference_code>/success', views.confirmTransactionStatus),
    path('receive/', views.ReceivePayment),
    path('register/', views.RegistrationView, name='registration'),
    # LOGIN PAGE
    path('login/', views.LoginView, name='login'),
]
