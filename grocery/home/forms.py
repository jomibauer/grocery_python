from django import forms

from django import forms
from django.contrib.auth.models import User
from django.apps import apps



class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


class ShopUserForm(forms.ModelForm):
	class Meta:
		model = apps.get_model("login", model_name="shopUser")
		fields = ('lst',)


class AddListItemForm(forms.Form):
	items = forms.CharField(max_length=200, label="items", widget=forms.TextInput(attrs={'height': 80}))