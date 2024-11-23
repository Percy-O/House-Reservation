from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest
from django.contrib.auth.decorators import login_required
from account.models import User
from Agent import models,forms
from Agent.models import House
from Chat.models import Message

from django.conf import settings

# Create your views here.

@login_required(login_url='account:login')
def dashboard(request):
	# All House
	houses = models.House.objects.filter(agent=request.user) 

	# All Message sent to agent by the tenant
	messages = Message.objects.filter(agent=request.user,viewed=False)
	
	# All Reserved House
	house_reserved = models.House.objects.filter(status=True)

	context={'houses':houses,'messages':messages,'house_reserved':house_reserved}
	return render(request,'Agent/dashboard.html',context)

@login_required(login_url='account:login')
def addType(request):

	types= models.Type.objects.all()

	if request.method == 'POST':

		form = forms.TypeForm(data=request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('.')
		else:
			messages.error(request,'Unable to save rooms')
	else:

		form = forms.TypeForm()


	context={'types':types,'form':form}
	return render(request,'Agent/type.html',context)


@login_required(login_url='account:login')
def deleteType(request,id):
    
	# Get Semester
    get_type = models.Types.objects.get(id=id)
    cancel = 'Type'
	
    if request.method == 'POST':
	    # Delete Semester
        get_type.delete()
		
        if get_type:
            # Success Messages
            messages.success(request,'Deleted Successfully!')
        else: messages.error(request,'Unable To Delete!')
		
        return redirect('Agent:type')

		
    context= {'obj':get_type,'cancel':cancel}
    return render(request,'Agent/delete.html',context)
	

@login_required(login_url='account:login')
def updateType(request,id):
	
    verify = 'update'
	
	#All Semesters
    types=models.Type.objects.all()
	
	#Get Semester
    get_type = models.Type.objects.get(id=id)
    form = forms.TypeForm(instance=get_type)
	
    if request.method == 'POST':
        type_name = request.POST.get('name')
		
		# Update Semester
        get_type.name = type_name
        get_type.save()
        if get_type:
            messages.success(request,'House Type Updated Successfully!')
        else:
            messages.error(request,'Unable To Update House Type!')
        return redirect('Agent:type')
    
    context={'verify':verify,'form':form,'types':types}
    return render(request,'Agent/type.html',context)


@login_required(login_url='account:login')
def addHouse(request):
	# house_form=None
	types = models.Type.objects.all()	
	form = forms.HouseForm()
	if request.method == 'POST':

		# Get Data From The Form
		house_name = request.POST.get('name')
		get_house_type = request.POST.get('house_type')
		house_type = models.Type.objects.get(id=get_house_type)
		house_room = request.POST.get('room')
		house_rent = request.POST.get('house_rent')
		house_details = request.POST.get('house_details')
		images = request.FILES.getlist('image')
		house_agent = request.user

		# Save Data Get From Form
		house=House.objects.create(
				name = house_name,
				house_type = house_type,
				room = house_room,
				house_rent = house_rent,
				house_details = house_details,
				agent= house_agent,
			)

		# Looping Through Images
		for image in images:
			house_image = models.House_Image.objects.create(

				house_name = house_name,
				image = image
				)
			# Save House Image
			house_image.save()
		# Save House
		house.save()
		messages.success(request,'House Details Successfully Saved!')

		# Passing images back to the House table

		# Filter Image QuerySet
		house_image = models.House_Image.objects.filter(house_name= house_name)

		# Get House
		house = models.House.objects.get(name=house_name)

		# Loop Images into the house table 
		for house_image in house_image:
			# Add image into the house table
			house.houseimage.add(house_image)


	context={'types':types,'form':form}
	return render(request,'Agent/house.html',context)

@login_required(login_url='account:login')
def allHouse(request):

	houses = models.House.objects.filter(agent = request.user)


	context={'houses':houses}
	return render(request,'Agent/all_house.html',context)

@login_required(login_url='account:login')
def deleteHouse(request,id):
    
	# Get Semester
    house = models.House.objects.get(id=id)
    cancel = 'House'
	
    if request.method == 'POST':
	    # Delete Semester
        house.delete()
		
        if house:
            # Success Messages
            messages.success(request,'Deleted Successfully!')
        else: messages.error(request,'Unable To Delete!')
		
        return redirect('Agent:all_house')
		
		
    context= {'obj':house,'cancel':cancel}
    return render(request,'Agent/delete.html',context)
	

@login_required(login_url='login')
def updateHouse(request,id):
	
    verify = 'update'
	
	#Get Semester
    house = models.House.objects.get(id=id)
    form = forms.HouseForm(instance=house)
	
    if request.method == 'POST':

        house_name = request.POST.get('name')
        get_house_type = request.POST.get('house_type')
        house_type = models.Type.objects.get(id=get_house_type)
        house_room = request.POST.get('room')
        house_rent = request.POST.get('house_rent')
        house_details = request.POST.get('house_details')
        images = request.FILES.getlist('image')

		# Update House
        house.name = house_name
        house.house_type = house_type
        house.room = house_room
        house.house_rent = house_rent
        house.house_details = house_details

        for image in images:
        	house_image = models.House_Image.objects.get(house_name=house_name)
			
			# Update image
        	house_image.image = image
			# Save House Image
        	house_image.save()

        house.save()
        if house:
       		messages.success(request,'House Details Successfully Updated!')
        else:
            messages.error(request,'Unable To Update House Details!')
        return redirect('Agent:all_house')

        house_image = models.House_Image.objects.filter(house_name= house_name)
		
		# Get House
        house = models.House.objects.get(name=house_name)

		# Loop Images into the house table 
        for house_image in house_image:
        	
			# Add image into the house table
        	house.houseimage.add(house_image)    
    
    context={'verify':verify,'form':form}
    return render(request,'Agent/house.html',context)




def initiate_payment(request:HttpRequest) -> HttpResponse:

	if request.method == 'POST':
		payment_form = forms.HousePaymentForm(request.POST)

		if payment_form.is_valid():
			payment_form = payment_form.save()
			payments = models.HousePayment.objects.filter(amount=payment_form.amount)
			for payment in payments:
				payment=payment
			return render(request,'Agent/make_payment.html',{
													'payment':payment,
													'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY
													})
	else:
		payment_form = forms.HousePaymentForm()
	return render(request,'Agent/initiate_payment.html',{'payment_form':payment_form})



def verify_payment(request:HttpRequest, ref:str) -> HttpResponse:
	
	# All Message sent to agent by the tenant
	# messages = Message.objects.filter(agent=request.user,viewed=False)

 	payment = get_object_or_404(models.HousePayment,ref=ref)
 	verified = payment.verify_payment()

 	if verified:
 		messages.success(request,"Verification Successful")
 	else: 
 		messages.error(request,"Verification Failed")
 	return redirect('Agent:dashboard')




	

