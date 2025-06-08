from django import forms
from .models import Item, Booking
from django.contrib.auth.models import User


class ReportForm(forms.Form):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), empty_label="All Items", required=False)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_staff']
        widgets = {'password': forms.PasswordInput()}

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'is_staff']

class BookingAdminForm(forms.ModelForm):
    start_date = forms.DateField(label='Start Date')
    start_time = forms.TimeField(label='Start Time')
    end_date = forms.DateField(label='End Date')
    end_time = forms.TimeField(label='End Time')
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='User')
    is_overdue = forms.BooleanField(initial=False, required=False, label='Is Overdue')
    item = forms.ModelChoiceField(queryset=Item.objects.all(), label='Item')

    class Meta:
        model = Booking
        fields = ['item', 'user', 'start_date', 'start_time', 'end_date', 'end_time', 'is_overdue']

class BookingUserForm(forms.ModelForm):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(label='Start Time', widget=forms.TimeInput(attrs={'type': 'time'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_time = forms.TimeField(label='End Time', widget=forms.TimeInput(attrs={'type': 'time'}))


    class Meta:
        model = Booking
        fields = [ 'start_date', 'start_time', 'end_date', 'end_time']

class CreateItemForm(forms.ModelForm):
    class Meta: 
        model = Item
        fields = '__all__'

class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
