from django import forms
from .models import Sample, User



class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
class SampleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'
        #clickable calendar for date fields
        widgets = {
            'reception_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'preparation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class UserForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        exclude = ['account']
        widgets = {
            'submission_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'confidentiality': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }