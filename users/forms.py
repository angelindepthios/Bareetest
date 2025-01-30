from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class UserRegistForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    full_name = forms.CharField(max_length=100, required=True)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), required=True
    )  # Mengganti age menjadi birth_date dengan widget date picker
    gender = forms.ChoiceField(choices=[
        ('male', 'Male'), 
        ('female', 'Female'), 
    ], required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    skintype = forms.ChoiceField(choices=[
        ('combination', 'Combination'), 
        ('normal', 'Normal'), 
        ('oily', 'Oily'), 
        ('dry', 'Dry'), 
        ('sensitive', 'Sensitive')
    ], required=True)
    profile_photo = forms.ImageField(required=False)  # Menggunakan ImageField untuk upload foto

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'birth_date', 'gender', 'phone_number', 'skintype', 'profile_photo', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")  
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)