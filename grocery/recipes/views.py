from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .util import find_domain, get_from_all_recipes
from .forms import AddRecipeForm


@login_required(login_url=('/login/'))
def view_index(request, ):
	form = AddRecipeForm()
	user = User.objects.get(pk=int(request.session["db_id"]))
	recipes = user.shopuser.get_recipe_names()

	return render(request, 'recipes/index.html', {'form': form, 'recipes': recipes})


@login_required(login_url=('/login/'))
def process_add_recipe(request, ):
	if request.method == "POST":
		form = AddRecipeForm(data=request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			recipe_url = form_data['recipe_url']
			recipe_name = form_data['recipe_name']
			recipe_index = form_data['recipe_index']
			'''
			messages.error(request, 'url: ' + recipe_url + "|||| name: " + recipe_name)
			return redirect('/recipes/')


			'''

			user = User.objects.get(pk=int(request.session["db_id"]))

			recipe_lst = user.shopuser.get_recipes()
			recipe_name_lst = user.shopuser.get_recipe_names()

			recipe_lst[int(recipe_index)] = recipe_url
			recipe_name_lst[int(recipe_index)] = recipe_name

			user.shopuser.save_recipes(recipe_lst)
			user.shopuser.save_recipe_names(recipe_name_lst)
			user.shopuser.save()
			user.save()

			return redirect('/recipes/')


@login_required(login_url=('/login/'))
def view_my_recipe(request, ):
	recipe_index = request.GET.get('rn')

	user = User.objects.get(pk=int(request.session["db_id"]))
	recipes = user.shopuser.get_recipes()
	recipe_names = user.shopuser.get_recipe_names()

	url = recipes[int(recipe_index)]
	domain = find_domain(url)

	if domain == 'allrecipes':
		my_recipe_name = recipe_names[int(recipe_index)]
		my_recipe = get_from_all_recipes(url)
		ingredients = my_recipe[0]
		steps = my_recipe[1]
		return render(request, 'recipes/my_recipe.html', {'recipe_name': my_recipe_name, 'ingredients': ingredients,
														  'steps': steps})
	else:
		return render(request, 'recipes/my_recipe_url.html', {'recipe_url': url})
