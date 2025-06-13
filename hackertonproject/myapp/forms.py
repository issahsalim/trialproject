from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from .models import USERACCOUNT


class userForm(UserCreationForm):
    Course=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Your Course',}) ,label='Course' )

    password1= forms.CharField(
         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','id':'password'}),
         label='Password'
    )

    password2= forms.CharField(
         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm','id':'c_password'}),
         label='ConfirmPassword'
    )

    
    class Meta:
        model = USERACCOUNT
        fields = ['username', 'first_name', 'last_name', 'email', 'Course', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': f'{field.label}'}) 

    def clean(self):
         cleaned_data=super().clean()
         valid_course=cleaned_data.get('Course')
         if len(valid_course)<3:
             self.add_error('Course',"Please course must be above three characters") 
         return cleaned_data
    
    