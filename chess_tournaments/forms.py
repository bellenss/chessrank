from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Tournament

class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = '__all__'  # Includes all model fields
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'tie_breaks': forms.Textarea(attrs={'rows': 3}),
        }

