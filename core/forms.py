from django import forms
from .models import Sample

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        #clickable calendar for date fields
        widgets = {
            'reception_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preparation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }