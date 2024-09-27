from .login import *
from .views import *
from django.urls import *
urlpatterns = [
    path('auth/login', login_view, name="login"), 
  
    ]
