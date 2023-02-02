from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',hello_index),
    path('pid/<str:pid>',query_patient_by_id),
    path('sl1/',sl1),
    path('sl2/',sl2),
    path('sl3/',sl3),
    path('sl4/',sl4),
    path('userlist/',user_list),
    path('add_user/',add_user),
    path('delete_user/', delete_user), 
    path('update_user/',update_user),
    path('redunt/',redunt_user),
    path('count_disease/',count_disease),
    path('count_anatomy/',count_Anatomy),
    path('pinfo/',pinfo),
    path('user2/',user2)
    
]