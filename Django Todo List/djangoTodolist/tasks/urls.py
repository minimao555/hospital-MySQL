from django.urls import path
from . import views

urlpatterns = [
	# root path
	path('', views.index, name='list'),
	path('update/<int:update_id>', views.update, name='update'),
	path('delete/<int:del_id>', views.delete, name='delete')
]
