from django import forms
from Tenant import models

class HousePaymentForm(forms.ModelForm):

	class Meta():

		model = models.HousePayment
		fields=['amount','email']

