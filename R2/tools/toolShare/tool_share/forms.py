from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from tool_share.models import ToolUser
from django.contrib.auth import authenticate, hashers

class RegistrationForm(ModelForm):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput(render_value=False))#label=(unicode('Password')), widget=forms.PasswordInput(render_value=False))
	passwordverify = forms.CharField(widget=forms.PasswordInput(render_value=False))#label=(unicode('Verify_Password')), widget=forms.PasswordInput(render_value=False))
	name = forms.CharField(max_length=25)
	zipCode = forms.IntegerField()
	pickup = forms.CharField(required=False)
	class Meta:
		model = ToolUser
		exclude = ('user')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('That username is already taken. Please select another.')

	def clean_zipCode(self):
		zipCode = self.cleaned_data['zipCode']
		if zipCode > 99999:
			raise forms.ValidationError('Zip Code is too large.')
		return zipCode

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('That email is already in use. Please use another.')

	def clean_pickup(self):
		return self.cleaned_data['pickup']
	
	def clean (self):
		try:
			username=self.cleaned_data['username']
		except KeyError:
			raise forms.ValidationError('Please enter a username')
		try:
			username=self.cleaned_data['email']
		except KeyError:
			raise forms.ValidationError('Please enter an email')
		try:
			username=self.cleaned_data['password']
		except KeyError:
			raise forms.ValidationError('Please enter a password')
		try:
			username=self.cleaned_data['passwordverify']
		except KeyError:
			raise forms.ValidationError('Please verify your password')
		try:
			username=self.cleaned_data['name']
		except KeyError:
			raise forms.ValidationError('Please enter your full name')
		try:
			username=self.cleaned_data['address']
		except KeyError:
			raise forms.ValidationError('Please enter your address')
		try:
			username=self.cleaned_data['zipCode']
		except KeyError:
			raise forms.ValidationError('Please enter your zip code')
		
		password = self.cleaned_data['password']
		passwordverify = self.cleaned_data['passwordverify']
		if password != passwordverify:
			raise forms.ValidationError('Passwords do not match.')

		return self.cleaned_data

class LoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput(render_value=False))
	def clean_username(self):
		try:
			self.cleaned_data['username']
		except KeyError:
			raise forms.ValidationError("Please enter a username.")
		return self.cleaned_data['username']

	def clean_password(self):
		try:
			self.cleaned_data['password']
		except KeyError:
			raise forms.ValidationError("Please enter a password.")
		return self.cleaned_data['password']

	def clean(self):
		#first make sure the user actually typed in both fields
		try:
			username = self.cleaned_data['username']
			password = self.cleaned_data['password']
		except KeyError:
			raise forms.ValidationError("Invalid username or password.")
		
		#next, check whether or not a user with that username exists
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise forms.ValidationError("Invalid username or password.")
		
		#finally, check if the password matches
		if hashers.check_password(password, user.password):
			return self.cleaned_data
		else:
			raise forms.ValidationError("Invalid username or password.")

class ToolRegistrationForm(forms.Form):
	toolType=forms.CharField()
	description=forms.CharField(max_length=200)
	
	def clean_toolType(self):
		if self.cleaned_data['toolType'] == "":
			raise forms.ValidationError('Please enter a tool type.')

		return self.cleaned_data['toolType']

class ShedCreationForm(forms.Form):
	name = forms.CharField(max_length=30)
	motto = forms.CharField(max_length=100)
	description = forms.CharField(max_length=1000)

	def clean(self):
		try:
			self.cleaned_data['name']
		except KeyError:
			raise forms.ValidationError('Please enter a name.')
		try:
			self.cleaned_data['motto']
		except KeyError:
			raise forms.ValidationError('Please enter a motto.')
		try:
			self.cleaned_data['description']
		except KeyError:
			raise forms.ValidationError('Please enter a description.')
		return self.cleaned_data

class MessageForm(forms.Form):
	reciever = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))
	subject = forms.CharField(max_length=80)
	message = forms.CharField(max_length=80)

	def clean_subject(self):
		try:
			self.cleaned_data['subject']
		except KeyError:
			raise forms.ValidationError('Please enter a subject.')
		return self.cleaned_data['subject']

	def clean_message(self):
		try:
			self.cleaned_data['message']
		except KeyError:
			raise forms.ValidationError('Please enter a message.')
		return self.cleaned_data['message']

class EditUserForm(forms.Form):
	name = forms.CharField()
#	email = forms.EmailField()
	password = forms.CharField(required=False,widget=forms.PasswordInput(render_value=False))#label=(unicode('Password')), widget=forms.PasswordInput(render_value=False))
	passwordverify = forms.CharField(required=False,widget=forms.PasswordInput(render_value=False))#label=(unicode('Verify_Password')), widget=forms.PasswordInput(render_value=False))
	address = forms.CharField()
	zipCode = forms.IntegerField()
	pickup = forms.CharField(required=False)

	def clean_zipCode(self):
		zipCode = self.cleaned_data['zipCode']
		if zipCode > 99999:
			raise forms.ValidationError('Zip Code is too large.')
		return zipCode

#	def clean_email(self):
#		email = self.cleaned_data['email']
#		try:
#			User.objects.get(email=email)
#		except User.DoesNotExist:
#			return email
#
#		raise forms.ValidationError('That email is already in use. Please use another.')

	def clean(self):
		try:
			password = self.cleaned_data['password']
			passwordverify = self.cleaned_data['passwordverify']
			if password != passwordverify:
				raise forms.ValidationError('Passwords do not match.')
			return self.cleaned_data

		except KeyError:
			#one of the password fields was left blank
			self.cleaned_data['password'] = ''
			self.cleaned_data['passwordverify'] = ''
			return self.cleaned_data

		