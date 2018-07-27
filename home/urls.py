from django.urls import path, include
from home import views
urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.RegistrationView, name='registration')
]
