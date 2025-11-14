from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = [
            'emp_id', 'first_name', 'last_name', 'email', 
            'department', 'designation', 'date_joined',
            'username', 'password'
        ]
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'emp_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
        }

