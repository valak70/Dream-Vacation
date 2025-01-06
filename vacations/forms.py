from django import forms
from .models import DreamVacation, Comment

class VacationForm(forms.ModelForm):
    category = forms.ChoiceField(choices=DreamVacation.CATEGORY_CHOICES)

    class Meta:
        model = DreamVacation
        fields = ['title', 'description', 'category', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
