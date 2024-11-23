from django.db import models
from django.contrib.auth.models import AbstractUser
# from Chat.models import Message


class User(AbstractUser):

	GENDER_CHOICES = [

		('M','Male'),
		('F','Female')
	]

	USER_CHOICES = [ 

		('A','Agent'),
		('T','Tenant')
	]

	name = models.CharField(max_length=255)
	gender = models.CharField(choices=GENDER_CHOICES,max_length=2)
	usertype = models.CharField(choices=USER_CHOICES,max_length=2)
	is_tenant= models.BooleanField(default=False)
	is_agent= models.BooleanField(default=False)
	phone_num = models.IntegerField(null=True)
	# message=models.ManyToManyField(Message,blank=True)
	avatar= models.ImageField(upload_to='account/images/',default='../static/images/avatar.png')



	def approve_tenant(self):

		self.is_tenant = True
		self.save()
	def approve_agent(self):

		self.is_agent = True
		self.save()

	

