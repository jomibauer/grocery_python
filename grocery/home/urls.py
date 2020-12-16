from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_index, name='index'),
	path('add_item', views.process_add_to_list, name='add_item_to_list'),
	path('remove_bought_item', views.process_remove_bought_item, name='remove_bought_item'),
	path('logout', views.process_logout, name='logout'),
]