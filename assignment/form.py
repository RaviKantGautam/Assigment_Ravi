from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, PasswordChangeForm
from django.core.validators import EmailValidator
from phonenumber_field.formfields import PhoneNumberField
from .models import *

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email','phn_no')
    def clean_email(self):
        """check if the email already exists"""
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email already exist')
        return email
    def clean_password2(self):
        """check if the both passwords match"""
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.client = True
        user.active = True
        user.save()

class requestCreate(forms.ModelForm):
    class Meta:
        model = Request_Table
        fields = ('request_type','city','state','pincode','mobile','request_desc')
        widgets = {
            'request_type':forms.CheckboxSelectMultiple(),
            # 'mobile':forms.TextInput(attrs={'class':'form-control','placeholder':'Mobile Number','pattern':'[0-9]{3}[0-9]{3}[0-9]{4}','title':'Invalid Phone Number'})
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }

class requestUpdate(forms.ModelForm):
    class Meta:
        model = Request_Table
        fields = ('status','remarks')
