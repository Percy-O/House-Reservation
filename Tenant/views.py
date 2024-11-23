from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.db.models import Q 
from account.models import User
from Agent import models,forms
from Tenant import models,forms
from Chat.models import Message

# Create your views here.
@login_required(login_url='account:login')
def dashboard(request):

	# messages = Message.objects.filter(user=request.user,viewed=False)
	messages=None
	houses = models.House.objects.filter(user_message__user=request.user)
	for house in houses:
		house_agent = house.agent
		messages= house.user_message.filter(viewed=False,agent=house_agent).exclude(Q(user=request.user))

	context={'messages':messages}
	return render(request,'Tenant/dashboard.html',context)

@login_required(login_url='account:login')
def getHouse(request):


	# Search For Houses
	q = request.GET.get('q') if request.GET.get('q') !=None else ''
	

	# All Houses
	all_houses = models.House.objects.filter(
		Q(status=False)|
		Q(name__icontains=q)|
		Q(agent__name__icontains=q)
		
		).order_by('-agent')

	# Check if searched house exists
	if all_houses.exists() and q == request.GET.get('q'):
		messages.success(request,'House Found!')
	else:
		if not(all_houses.exists()) and q ==request.GET.get('q'):
			messages.error(request,f'Could Not Find House "{q}"')


	# Get Page 1
	page = request.GET.get('page',1)

	# Data Per Page
	paginator = Paginator(all_houses, 3)

	try:
		houses = paginator.page(page)
	except PageNotAnInteger:
		houses = paginator.page(1)
	except EmptyPage:
		houses = paginator.page(paginator.num_pages)

	
	context={'houses':houses}
	return render(request,'Tenant/all_houses.html',context)

@login_required(login_url='account:login')
def bookHouse(request):



	id = request.session.get('house_id')
	get_house = models.House.objects.get(id=id)

	# Get Payment
	payment = get_object_or_404(models.HousePayment,user=request.user)

	# Get Information of the house
	if request.method == 'POST':

		if get_house.status == True:
			messages.error(request,f'"{request.user.username}" House already booked!')
		else:
			if payment.verified == True: 
				# Book House
				booked = models.BookHouse.objects.create(
						user = request.user,
						booked_house = get_house,
					).save()
				get_house.approve_house()
				messages.success(request,f'"{request.user.username}" House Successfully Booked!')
			else:
				messages.warning(request,'YOU NEED TO PAY FOR THIS HOUSE')
				return redirect('Tenant:initiate_payment')



	context = {'house':get_house}
	return render(request,'Tenant/book_house.html',context)


def initiate_tenant_payment(request:HttpRequest,house:str) -> HttpResponse :

	# Get House Price and User Email

	get_house = models.House.objects.get(name=house)
	request.session['house_id'] = get_house.id

	# HousePayment
	# payment = models.HousePayment.objects.get(verified=False)
	if get_house.status == False :
		if request.method == 'POST':
			amount = request.POST.get('amount')
			email=request.POST.get('email')
			payment_form = models.HousePayment.objects.create(
					user = request.user,
					amount= amount,
					email = email,
					house_name=get_house.name,
				)

			if payment_form:
				payment_form= payment_form.save()
				# Get Payment Details
				payment = models.HousePayment.objects.get(amount=get_house.house_rent,house_name=get_house.name)
				context={
						'payment':payment,
						'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY
						}
				return render(request,'Tenant/make_payment.html',context)
			else:
				messages.error(request,'Your Payment Form Is Invalid!')
	else:
		payment = models.HousePayment.objects.get(verified=True,user=request.user)
		if payment.verified == True and payment.house_name == get_house.name:
			if request.method == 'GET':
				return redirect('Tenant:book_house')


	context={'get_house':get_house}
	return render(request,'Tenant/initiate_payment.html',context)

def verify_tenant_payment(request:HttpRequest, ref:str) -> HttpResponse:

	payment = get_object_or_404(models.HousePayment,ref=ref)

	verified = payment.verify_payment()

	if verified:

		messages.success(request,'Payment Verified and is Successful!')
	else:

		messages.error(request,'Unable To Verify Payment!')
	return redirect('Tenant:book_house')






	




