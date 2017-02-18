from django.conf.urls import  include, url
from loginapp import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', login),
    url(r'^logout/$', views.logout_page, name='logout_page'),
    url(r'^accounts/login/$', login), # If user is not login it will redirect to login page
    url(r'^register/$', views.register, name='register'),
    url(r'^register/success/$', views.register_success, name='register_success'),
    url(r'^home/$', views.home, name='home'),
]
