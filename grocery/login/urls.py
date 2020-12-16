from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
	path('registration', views.view_registration, name="registration"),
    path('validate_login', views.process_validate_login, name='validate_login'),
	path('register_user', views.process_register_user, name="register_user"),
]