from django.urls import path

from . import views

urlpatterns = [
	path('', views.view_index, name='index'),
	path('my_recipe/', views.view_my_recipe, name='my_recipe'),
	path('add_recipe/', views.process_add_recipe, name='add_recipe'),

]