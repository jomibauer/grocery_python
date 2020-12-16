from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone


from .forms import AddListItemForm


@login_required(login_url=('/login/'))
def view_index(request,):
	user = User.objects.get(pk=int(request.session["db_id"]))
	session_scope = request.session.items()
	try:
		username = request.session['username']
		form = AddListItemForm()
		lst = user.shopuser.get_lst()
		date_bought = user.shopuser.get_date_bought().date()
		just_bought = user.shopuser.get_just_bought()


	except KeyError:
		messages.error(request, 'something went wrong, please login again')
		logout(request)
		return redirect('/login/')

	return render(request, "home/index.html", {"username": username, "form": form, "lst": lst,
											   "date": date_bought, "session_scope": session_scope,
											   'just_bought': just_bought})


@login_required(login_url=('/login/'))
def process_add_to_list(request,):
	if request.method == "POST":
		form = AddListItemForm(data=request.POST)
		if form.is_valid():
			#  get items from the form, split on commas in case user adds multiple items to the list
			item_data = form.cleaned_data
			items = (item_data['items']).split(',')
			#  get the user, update the session lst with added items, then save the new session list to the user
			user = User.objects.get(pk=int(request.session["db_id"]))
			temp_lst = user.shopuser.get_lst()
			temp_lst.extend(items)

			user.shopuser.save_lst(temp_lst)
			user.shopuser.save()
			user.save()
			return redirect("/home/")


@login_required(login_url=('/login/'))
def process_remove_bought_item(request,):
	if request.method == "POST":
		user = User.objects.get(pk=int(request.session["db_id"]))
		#  get list of purchased items
		tbr_list = request.POST.getlist('item')
		#  figure out if we update or overwrite the just_bought list by comparing now_date with date_bought
		date_bought = user.shopuser.get_date_bought().date()
		now_date = timezone.now().date()
		if now_date > date_bought:
			# if now is later than our previous date bought, overwrite just_bought and update our date_bought
			user.shopuser.save_just_bought(tbr_list)
			user.shopuser.update_date_bought(now_date)
		else:
			#  if now is not later than our date bought, add to our just_bought list by extending it
			new_just_bought = user.shopuser.get_just_bought()
			new_just_bought.extend(tbr_list)
			user.shopuser.save_just_bought(new_just_bought)
		# then, remove items in tbr from lst.
		new_lst = [item for item in user.shopuser.get_lst() if item not in tbr_list]
		if len(new_lst) == 0:
			new_lst = [None]

		#  save then redirect back to homepage
		user.shopuser.save_lst(new_lst)
		user.shopuser.save()
		user.save()

		return redirect("/home/")


def process_logout(request,):
	if request.method == "POST":
		logout(request)
		return redirect('/login/')

