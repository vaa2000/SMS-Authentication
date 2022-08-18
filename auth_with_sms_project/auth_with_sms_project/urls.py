from django.contrib import admin
from django.urls import path
from eoapp.views import home
from auapp.views import ulogin,ulogout,usignup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('ulogin/', ulogin, name='ulogin'),
    path('ulogout/', ulogout, name='ulogout'),
    path('usignup/', usignup, name='usignup'),
 
]
