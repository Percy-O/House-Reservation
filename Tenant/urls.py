from django.conf.urls import url
from django.urls import path
from Tenant import views


app_name = 'Tenant'

urlpatterns = [
		
		url(r'^dashboard/$',views.dashboard,name='dashboard'),
		url(r'^all/house/$',views.getHouse,name='all_house'),
		url(r'^house/book/$',views.bookHouse,name='book_house'),
		url(r'^initiate/(?P<house>[A-Za-z \s]+)/payment/$',views.initiate_tenant_payment,name='initiate_payment'),
		url(r'^verify/ref/(?P<ref>[\w]+)/$',views.verify_tenant_payment,name='verify_payment'),



]