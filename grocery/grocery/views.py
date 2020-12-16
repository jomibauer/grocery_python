from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponseRedirect('/login/')


@login_required(login_url=('/login/'))
def process_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')