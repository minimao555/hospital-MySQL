from django.shortcuts import render, redirect
from django.core import exceptions
from django.contrib import messages
from .models import Task
from .forms import *
import datetime

# Create your views here.
def index(request):
	tasks = Task.objects.all()

	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/')
	return render(request, 'index.html', {'tasks': tasks, 'today': datetime.date.today()})


def update(request, update_id: int):
	task = Task.objects.get(pk=update_id)
	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid:
			form.save()
		return redirect('/')

	return render(request, 'update.html', {'form': form})


def delete(request, del_id: int):
	try:
		task = Task.objects.get(pk=del_id)
		task.delete()
	except exceptions.ObjectDoesNotExist:
		messages.error(request, 'task id: {} does not exist.'.format(del_id))

	return redirect('/')
