import secrets
from Tenant.Paystack import PayStack
from django.db import models
from account.models import User
from Agent.models import House



# Create your models here.



class ViewHouse(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	house = models.ForeignKey(House,on_delete=models.CASCADE)

class BookHouse(models.Model):

	user= models.ForeignKey(User,on_delete=models.CASCADE)
	booked_house = models.ForeignKey(House,on_delete=models.CASCADE)
	booked_date= models.DateTimeField(auto_now_add=True)

	def __str__(self):

		return '%s %s'%(self.user.username,self.booked_house.name)

class HousePayment(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	house_name=models.CharField(max_length=255,null=True)
	amount = models.PositiveIntegerField()
	email = models.EmailField()
	ref = models.CharField(max_length=255)
	verified = models.BooleanField(default=False)
	date_paid = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date_paid']

	def __str__(self):

		return f'{self.user.username} Paid {self.amount} for {self.house_name}'

	def save(self,*args,**kwargs) ->None:

		while not self.ref:
			ref = secrets.token_urlsafe(10)
			check_ref = HousePayment.objects.filter(ref=ref)

			if not check_ref:
				self.ref = ref
		super().save(*args,**kwargs)

	def amount_value(self)-> int:

		return self.amount * 100
		
	def verify_payment(self):
		paystack = PayStack()
		status,result = paystack.verify_payment(self.ref,self.amount)
		if status:
			if result['amount'] / 100 == self.amount:

				self.verified = True
			self.save()
			
		if self.verified:
			return True

		else:

			return False







