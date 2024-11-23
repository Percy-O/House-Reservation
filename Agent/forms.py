from django import forms
from Agent import models

class HouseForm(forms.ModelForm):

	class Meta():

		model = models.House
		# exclude = ['status','date_posted']
		fields = ['name','house_type','room','house_rent','house_details','agent']
		# widgets={
		# 	'house_image':forms.FileInput(attrs={'multiple':True})
		# }

class HouseImageForm(forms.ModelForm):
	model = models.House_Image
	fields = '__all__'


class TypeForm(forms.ModelForm):

	class Meta():

		model = models.Type
		fields='__all__'

class HousePaymentForm(forms.ModelForm):

	class Meta():
		model = models.HousePayment
		# exclude= ['verified','date_paid','ref']
		fields = ['amount','email']