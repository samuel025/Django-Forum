from django import forms
from .models import Comment


class AddComment(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']
		labels = {
			'body': 'Enter Your Comment',			
		}