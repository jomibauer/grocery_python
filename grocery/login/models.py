from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

import json
import datetime




class shopUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email = models.CharField(max_length=100)

	lst = models.CharField(max_length=200)
	just_bought = models.CharField(max_length=200)
	#  this may be a mistake!! for some reasomn i had to chnag ethe default to be timezone.now instead of
	#  timezone.now().date
	date_bought = models.DateTimeField(default=timezone.now)
	recipes = models.CharField(max_length=200, default=json.dumps([
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																]))
	recipe_names = models.CharField(max_length=200, default=json.dumps([
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																	'empty',
																]))

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			shopUser.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.shopuser.save()

	def save_lst(self, lst):
		if lst[0] is None:
			lst = lst[1:]
		self.lst = json.dumps(lst)

	def get_lst(self):
		return json.loads(self.lst)

	def save_just_bought(self, just_bought):
		self.just_bought = json.dumps(just_bought)

	def get_just_bought(self):
		return json.loads(self.just_bought)

	def save_recipes(self, recipes):
		self.recipes = json.dumps(recipes)

	def get_recipes(self):
		return json.loads(self.recipes)

	def save_recipe_names(self, recipe_names):
		self.recipe_names = json.dumps(recipe_names)

	def get_recipe_names(self):
		return json.loads(self.recipe_names)

	def get_date_bought(self):
		return self.date_bought

	def update_date_bought(self, date_obj):
		self.date_bought = date_obj
		self.save()

	def reset_recipes(self):
		self.recipes = json.dumps([
									'empty',
									'empty',
									'empty',
									'empty',
									'empty',
									'empty',
									'empty',
								])
		self.recipe_names = json.dumps([
										'empty',
										'empty',
										'empty',
										'empty',
										'empty',
										'empty',
										'empty',
									])

