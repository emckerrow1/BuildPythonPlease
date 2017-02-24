from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from models import Projects, Solution, Notifications

class LoginForm(AuthenticationForm):
	username = forms.CharField(label="Username", max_length=30, 
							   widget=forms.TextInput(attrs={'class': 'form-control',
							   								 'name': 'username'}))

	password = forms.CharField(label="Password", max_length=30, 
							   widget=forms.PasswordInput(attrs={'class': 'form-control',
							   									 'name': 'password'}))

class UserForm(UserCreationForm):

	email = forms.EmailField(required=True, label="Email")
	password1 = forms.CharField(required=True,label="Password", max_length=30, 
							   widget=forms.PasswordInput(attrs={'class': 'form-control',
							   									 'name': 'password1'}))
	password2 = forms.CharField(required=True,label="Confirm", max_length=30, 
							   widget=forms.PasswordInput(attrs={'class': 'form-control',
							   									 'name': 'password2'}))

	class Meta:
		model = User
		fields = ("username", "email","first_name","last_name","password1","password2")

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		  
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'

	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user





class CreateProjectForm(forms.ModelForm):

	version = forms.ChoiceField(choices=[("Any","Any"), ("Python 3.4", "Python 3.4"), ("Python 2.7", "Python 2.7"), ("Python 2.6", "Python 2.6")])
	client = forms.ChoiceField(choices=[("Command-Line","Command-Line"), ("Django", "Django")])

	class Meta:
		model = Projects
		fields = ('title','version','client','description','payout',)

class FilterForm(forms.Form):

	search = forms.ChoiceField(choices=[
								("Open Projects", "Open Projects"),
								("Closed Projects", "Closed Projects"),
								("My Projects", "My Projects"),
								("All Projects", "All Projects"),
						])

	#class Meta:
	#	model = Filter
	#	fields = ('search',)

class SolutionForm(forms.ModelForm):

	solution = forms.CharField(required=True),

	class Meta:
		model = Solution
		fields = ('solution',)


class PagesForm(forms.Form):

	page = forms.ChoiceField(
                choices=[("5", "5"), ("10", "10")], 
                widget=forms.Select(attrs={ 
                                   "onChange":'pagesform.submit()'})
                )
