from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from Agent import models




def home(request):
	# Search For Houses
	q = request.GET.get('q') if request.GET.get('q') !=None else ''
	

	# All Houses
	all_houses = models.House.objects.filter(
		Q(name__icontains=q)|
		Q(agent__name__icontains=q)
		
		).order_by('-date_posted')

	# Check if searched house exists
	if all_houses.exists() and q == request.GET.get('q'):
		messages.success(request,'House Found!')
	else:
		if not(all_houses.exists()) and q ==request.GET.get('q'):
			messages.error(request,f'Could Not Find House "{q}"')


	# Get Page 1
	page = request.GET.get('page',1)

	# Data Per Page
	paginator = Paginator(all_houses, 6)

	try:
		houses = paginator.page(page)
	except PageNotAnInteger:
		houses = paginator.page(1)
	except EmptyPage:
		houses = paginator.page(paginator.num_pages)

	
	context={'houses':houses}
	return render(request,'home.html',context)

def getHouse(request,house):

 	house= models.House.objects.get(name=house)
 	house_name= house.name
 	house_details = house.house_details

 	context={'house':house,'house_name':house_name,'house_details':house_details}
 	return render(request,'house.html',context)