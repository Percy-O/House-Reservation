from django.db import models
from account.models import User
from Chat.models import Message
from Agent import Paystack
import secrets
# Create your models here.


# class Room(models.Model):

# 	no_of_room = models.CharField(max_length=255)

# 	def __str__(self):

# 		return '%s'%(self.no_of_room)

class Type(models.Model):

	name = models.CharField(max_length=255,verbose_name="House Type")

	def __str__(self):

		return '%s'%(self.name)


class House(models.Model):

	name = models.CharField(max_length=255)
	house_type = models.ForeignKey(Type,on_delete=models.CASCADE)
	room = models.CharField(max_length=255)
	house_details = models.TextField(null=True)
	house_rent = models.IntegerField()
	houseimage= models.ManyToManyField('House_Image')
	user_message = models.ManyToManyField(Message, related_name='user_message',blank=True)
	agent = models.ForeignKey(User,on_delete=models.CASCADE)
	status = models.BooleanField(default=False)
	date_posted = models.DateTimeField(auto_now_add=True)


	def approve_house(self):
		self.status = True
		self.save()

	def __str__(self):

		return '%s'%(self.name)


class House_Image(models.Model):
	house_name = models.CharField(max_length=255,null=True)
	image = models.ImageField(upload_to='House/images/',null=True,blank=True,verbose_name="House Image")

	def __str__(self):

		return '%s'%(self.house_name)

class Agent_House(models.Model):
	agent = models.ForeignKey(User,on_delete=models.CASCADE)
	house = models.ManyToManyField(House)


	def __str__(self):

		return '%s'%(self.agent.name)


class HousePayment(models.Model):
	amount = models.PositiveIntegerField()
	ref = models.CharField(max_length=255)
	email= models.EmailField()
	verified = models.BooleanField(default=False)
	date_paid = models.DateTimeField(auto_now_add=True)


	class Meta:
		ordering = ['-date_paid']

	def __str__(self) -> str:
		return f'Payment:{self.amount}'


	def save(self,*args,**kwargs) ->None:
		while not self.ref:
			ref = secrets.token_urlsafe(10)
			object_with_similar_ref = HousePayment.objects.filter(ref=ref)

			if not object_with_similar_ref:
				self.ref = ref
		super().save(*args,**kwargs)


	def amount_value(self) -> int:
		return self.amount * 100

	def verify_payment(self):
		paystack = Paystack.PayStack()
		status,result = paystack.verify_payment(self.ref,self.amount)
		if status:
			if result['amount'] / 100 == self.amount:

				self.verified = True
			self.save()
		if self.verified:
			return True
		else:
			return False
