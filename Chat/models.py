from django.db import models
from account.models import User
# Create your models here.

class Message(models.Model):

	# tenant = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tenant")
	user  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user', null=True)
	agent = models.ForeignKey(User,on_delete=models.CASCADE,related_name='agent',null=True)
	house = models.CharField(max_length=255)
	message = models.TextField()
	message_created = models.DateTimeField(auto_now_add=True)
	message_updated = models.DateTimeField(auto_now=True)
	viewed = models.BooleanField(default=False)

	def message_viewed(self):
		self.viewed = True
		self.save()


	def __str__(self):

		return '%s'%(self.message)