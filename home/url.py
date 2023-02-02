from django.urls import path
from .views import *

urlpatterns = [
    path('', login),
    path('register/', register),
    path('logout/',logout),
    path('wrong/',wrong)
]