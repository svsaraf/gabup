from gab.models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Email'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'New Password'}))

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password',)

	def clean(self):
		if len(self.cleaned_data) < 4:
			raise forms.ValidationError("Something is missing!")
		firstn = self.cleaned_data['first_name']
		lastn = self.cleaned_data['last_name']
		usern = self.cleaned_data['email']
		try:
			usern = User.objects.get(email=usern)
			if usern > 0:
				raise forms.ValidationError("Email has already been used!")
		except User.DoesNotExist:
			pass
		if not firstn.isalpha():
			raise forms.ValidationError("Please use valid first name.")
		if not lastn.isalpha():
			raise forms.ValidationError("Please use valid last name.")
		return self.cleaned_data

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ()