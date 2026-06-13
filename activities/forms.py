from django import forms
from .models import Activity, WBSItem

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'project', 'name', 'description', 'optimistic_time', 'most_likely_time',
            'pessimistic_time', 'cost', 'priority', 'status', 'assigned_to',
            'start_date', 'end_date',
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget.attrs, 'get') or not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

class WBSForm(forms.ModelForm):
    class Meta:
        model = WBSItem
        fields = ['project', 'parent', 'name', 'description', 'progress', 'order']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget.attrs, 'get') or not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'
