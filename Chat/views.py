from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from Chat.models import Message
from Agent import models

# Create your views here.


@login_required(login_url='account:login')
def tenantMessage(request):

	messages=None
	houses = models.House.objects.filter(user_message__user=request.user)
	for house in houses:
		messages= house.user_message.filter(viewed=False)
	
	# Get all Chat
	chats = None
	house = models.House.objects.filter(user_message__user=request.user)
	for house in house:
		chats= house.user_message.all()

	# All Houses
	houses = models.House.objects.all()
	
	if request.method == 'POST':

		user = request.user
		get_House = request.POST.get('house')
		house= models.House.objects.get(name=get_House)
		if house:
			agent = models.User.objects.get(username=house.agent.username)
			get_Agent =agent
		else:
			messages.error(request,'House does not exists and cannnot find agent!')

		get_Message = request.POST.get('message') 


		# Create Message

		chat = Message.objects.create(

			user=user,
			agent = get_Agent,
			house = get_House,
			message = get_Message
		)
		chat.save()
		message = Message.objects.filter(house=get_House)
		for message in message:
			house.user_message.add(message)
		return redirect('.')


		

	context={'houses':houses,'chats':chats,'messages':messages}
	return render(request,'Chat/message.html',context) 

@login_required(login_url='account:login')
def tenantMessageview(request,pk):

	# Message sent to tenant
	messages=None
	houses = models.House.objects.filter(user_message__user=request.user)
	for house in houses:
		messages= house.user_message.filter(viewed=False)

	# All Chat
	chats = Message.objects.filter(id=pk)

	# When Message Viewed
	if chats.exists():
		for chat in chats:
			if request.user != chat.user:
				chat.message_viewed()

	# All Houses
	houses = models.House.objects.all()
	if request.method == 'POST':

		# Get all Details
		get_House = request.POST.get('house')
		house= models.House.objects.get(name=get_House)
		if house:
			agent = models.User.objects.get(username=house.agent.username)
			get_Agent =agent
		else:
			messages.error(request,'House does not exists and cannnot find agent!')
		get_User= request.user
		get_Message = request.POST.get('message') 


		# Create Message

		chat = Message.objects.create(

			user=get_User,
			agent=get_Agent,
			house = get_House,
			message = get_Message
		)
		chat.save()

		# Save all message into the specific house
		message = Message.objects.filter(house=get_House)
		for message in message:
			house.user_message.add(message)
		return redirect('.')

	context={'chats':chats,'houses':houses,'messages':messages}
	return render(request,'Chat/message.html',context)



# def agentInbox(request):

# 	messages = Message.objects.filter(agent=request.user)
# 	return render(request,'Dashboard/includes/_topbar.html',{'messages':messages})

@login_required(login_url='account:login')
def agentMessage(request,house):

	# Message Sent by tenant
	messages = Message.objects.filter(agent=request.user,viewed=False)

	agent_house = 'agent'

	# All Chat
	chats = Message.objects.filter(house= house)

	# When Message Viewed
	if chats.exists():
		for chat in chats:
			chat.message_viewed()

	# All Houses
	houses = models.House.objects.all()
	if request.method == 'POST':

		# Get all Details
		get_House = house
		house= models.House.objects.get(name=get_House)
		get_User= request.user
		get_Agent = request.user
		get_Message = request.POST.get('message') 


		# Create Message

		chat = Message.objects.create(

			user=get_User,
			agent=get_Agent,
			house = get_House,
			message = get_Message
		)
		chat.save()

		# Save all message into the specific house
		message = Message.objects.filter(house=get_House)
		for message in message:
			house.user_message.add(message)
		return redirect('.')

	context={'chats':chats,'houses':houses,'house':agent_house,'messages':messages}
	return render(request,'Chat/message.html',context)


def allAgentChat(request):

	all_house_chat = models.House.objects.filter(agent=request.user).exclude(user_message=None)

	context={'all_house_chat':all_house_chat}
	return render(request,'Chat/all_message.html',context)

def allTenantChat(request):

	all_house=models.House.objects.filter(user_message__user=request.user)
	
	
	all_house_chat = models.House.objects.filter(name__in=[all_house for all_house in all_house ]).exclude(~Q(user_message__user=request.user))

		
	context={'all_house_chat':all_house_chat}
	return render(request,'Chat/all_message.html',context)	





