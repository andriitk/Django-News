from django.urls import path
from .views import *

urlpatterns = [
    path('register/', SignUp.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]
