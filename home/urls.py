from django.urls import path, include
from home import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:id>/', views.getObject),
    path('receive/', views.ReceivePayment),
    path('register/', views.RegistrationView, name='registration'),
    # LOGIN PAGE
    path('login/', login, {'template_name': 'home/loginPage.html'}, name='login'),
]
