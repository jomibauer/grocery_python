from django import forms

from django import forms
from django.contrib.auth.models import User
from django.apps import apps

recipe_indices = [
	('0', 'Monday'),
	('1', 'Tuesday'),
	('2', 'Wednesday'),
	('3', 'Thursday'),
	('4', 'Friday'),
	('5', 'Saturday'),
	('6', 'Sunday'),
]


class AddRecipeForm(forms.Form):
	recipe_name = forms.CharField(max_length=200, label="Recipe name:", widget=forms.TextInput(attrs={'height': 80}))
	recipe_url = forms.CharField(max_length=200, label="Recipe URL:", widget=forms.TextInput(attrs={'height': 80}))
	recipe_index = forms.CharField(label="When do you want to cook this?", widget=forms.Select(choices=recipe_indices))

