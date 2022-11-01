from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder': "Add new task",
		'class': "input-group-ng"
	}))
	due_date = forms.DateField(widget=forms.TextInput(attrs={
		'type': "date"
	}), required=False)
	description = forms.CharField(widget=forms.TextInput(attrs={
		'class': "input-group-ng"
	}), required=False)

	class Meta:
		model = Task
		fields = '__all__'
