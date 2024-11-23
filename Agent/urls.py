from django.conf.urls import url
from django.urls import path
from Agent import views


app_name = 'Agent'

urlpatterns = [
		
		url(r'^dashboard/$',views.dashboard,name='dashboard'),
		url(r'^add/house/type/$',views.addType,name='type'),
		url(r'^add/house/type/(?P<id>[\d]+)/delete/$',views.deleteType,name='delete_type'),
		url(r'^add/house/type/(?P<id>[\d]+)/update/$',views.updateType,name='update_type'),

		url(r'^add/house/$',views.addHouse,name='house'),
		url(r'^all/house/$',views.allHouse,name='all_house'),
		url(r'^all/house/(?P<id>[\d]+)/delete/$',views.deleteHouse,name='delete_house'),
		url(r'^all/house/(?P<id>[\d]+)/update/$',views.updateHouse,name='update_house'),

		url(r'^initiate/payment/$',views.initiate_payment,name='initiate_payment'),
		path('<str:ref>/',views.verify_payment,name='verify_payment')
		# url(r'^(?P<ref>[A-Za-z])$',views.verify_payment,name="verifypayment"),


		





]