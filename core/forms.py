from django import forms
from .models import Sample, User

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        #clickable calendar for date fields
        widgets = {
            'reception_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preparation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'submission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'confidentiality': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }