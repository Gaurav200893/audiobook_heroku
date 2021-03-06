from django import forms

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	"""
		User Login Form
	"""

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		if username and password:
			user = authenticate(username=username, password=password)

			if not user:
				raise forms.ValidationError("This user does not exists")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user.is_active:
				raise forms.ValidationError("Incorrect password")

		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	"""
		User registration form
	"""

	email = forms.EmailField(label='Email address')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields=[
			'username',
			'email',
			'email2',
			'password'
		]

	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')

		if email2 != email:
			raise forms.ValidationError("Emails doesnt match.")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Email already exists")
		return email

class EditProfileForm(forms.ModelForm):
	"""
		Edit profile form
	"""

	first_name = forms.CharField(label='First Name')
	last_name = forms.CharField(label='Last Name')
	username = forms.EmailField(required=False,
    widget=forms.TextInput(attrs={'required': 'false',"disabled":"disabled"}),)
	email = forms.EmailField( required=False,
    widget=forms.TextInput(attrs={'required': 'false',"disabled":"disabled"}),)


	class Meta:
		model = User
		fields = ['first_name','last_name','username','email']


