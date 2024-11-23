from django import forms
from django.contrib.auth.forms import UserCreationForm
from account import models


class UserForm(UserCreationForm):

	class Meta():

		model = models.User
		fields = [
				'usertype',
				'name',
				'username',
				'phone_num',
				'email',
				'gender',
				'avatar',
				'password1',
				'password2',
				'is_tenant',
				'is_agent'
			]