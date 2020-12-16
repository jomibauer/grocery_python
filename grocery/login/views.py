from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from .models import shopUser


def view_index(request,):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/home/')
	else:
		form = AuthenticationForm()

		return render(request, "login/index.html", {"form": form, })


def view_registration(request,):
	form = UserCreationForm()

	return render(request, "login/registration.html", {"form": form, })


def process_validate_login(request,):
	if request.method == "POST" and "login" in request.POST:
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			login_info = form.cleaned_data
			user = authenticate(username=login_info['username'], password=login_info['password'])
			if user is not None:
				login(request, user)
				request.session['username'] = login_info['username']
				request.session['db_id'] = request.user.id
				request.session['lst'] = request.user.shopuser.get_lst()
				request.session['just_bought'] = request.user.shopuser.get_just_bought()
				return HttpResponseRedirect('/home/')
			else:
				messages.error(request, 'username or password not correct')
				return redirect('/login/')
		else:
			messages.error(request, 'username or password not correct')
			return redirect('/login/')
	else:
		messages.error(request, 'not post or login in post')
		return redirect('/login/')


def process_register_user(request,):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			if user is not None:
				login(request, user)
				#  Is this the best way to initialize our user -- I don't tink so.  I should look at the user creation
				#  form or google what the best thing to do is
				user.shopuser.save_lst([None])
				user.shopuser.save_just_bought([None])
				user.shopuser.save()

				# end extra user initialization

				request.session['username'] = username
				request.session['db_id'] = request.user.id
				request.session['lst'] = request.user.shopuser.get_lst()
				request.session['just_bought'] = request.user.shopuser.get_just_bought()
				return HttpResponseRedirect('/home/')
			else:
				messages.error(request, 'username or password not correct')
				return redirect('login:registration')
	else:
		return redirect('login:registration')


