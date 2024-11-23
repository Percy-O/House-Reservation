from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from account import forms, models

# Create your views here.

def register_user(request):

	if request.method =='POST':
		registered = False
		form = forms.UserForm(data=request.POST)


		if form.is_valid():

			form.save(commit=False)

			if 'avatar' in request.FILES:
				form.avatar = request.FILES['avatar']

			# if request.POST.get('usertype') == 'T' :
			# 	form.is_tenant = True
			# else:
			# 	if request.POST.get('usertype') is 'A' :
			# 		form.is_agent = True
			form.save()

			user_type = models.User.objects.get(usertype='T')

			if user_type.usertype == 'T':
				user_type.approve_tenant()
			else:
				if user_type.usertype == 'A':
					user_type.approve_agent()
			
			registered =True
			if registered == True:
				messages.success(request,'Account Successfully Created!')
				return redirect('account:login')
			else:
				messages.error(request,'Image File Invalid')
		else:

			messages.error(request,'Unable to save Form')
	else:

		form = forms.UserForm()


	context = {'form':form}
	return render(request,'account/register.html',context)



def login_user(request):

  	if request.method  == 'POST':

  		username = request.POST.get('username')
  		password = request.POST.get('password')

  		try:
  			models.User.objects.get(username=username)
  		except:
  			messages.error(request,'User does not exists!')
  		else:
  			user = authenticate(request,username=username,password=password)

  			if user is not None:
  				# Getting which User Either Tenant / Agent
  				user_get= models.User.objects.get(username=username)
  				if user_get.usertype == 'T':
  					login(request,user)
  					return redirect('Tenant:dashboard')
  				elif user_get.usertype == 'A':
  					login(request,user)
  					return redirect('Agent:dashboard')
  				else:
  					messages.error(request,'You dont have access to this page!')

  			else: messages.error(request,'Usename And Password Is Not Valid')

  	context ={}
  	return render(request,'account/login.html',context)


def logout_user(request):

	logout(request)
	return redirect('account:login')



