from django.db import models
from django.contrib.auth.models import User
from django import forms

class ItemType(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type

class ItemStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

class Item(models.Model):
    deviceSerialNumber = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50)
    type = models.ForeignKey('ItemType', on_delete=models.SET_NULL, null=True)
    CPU = models.CharField(max_length=50, null=True, blank=True)
    GPU = models.CharField(max_length=50, null=True, blank=True)
    RAM = models.CharField(max_length=50, null=True, blank=True)
    status = models.ForeignKey('ItemStatus', on_delete=models.SET_NULL, null=True)
    onsite = models.CharField(max_length=50, null=True, blank=True)
    audit = models.CharField(max_length=50, null=True, blank=True)
    item_inventory = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    dateOut = models.CharField(max_length=50, null=True, blank=True)
    dateReturn = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    warranty_duration = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Booking(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    is_overdue = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.item} by {self.user.username} ({self.start_date} {self.start_time} to {self.end_date} {self.end_time})"

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(label='Start Date')
    start_time = forms.TimeField(label='Start Time')
    end_date = forms.DateField(label='End Date')
    end_time = forms.TimeField(label='End Time')
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='User')
    is_overdue = forms.BooleanField(initial=False, required=False, label='Is Overdue')

    class Meta:
        model = Booking
        fields = ['item', 'user', 'start_date', 'start_time', 'end_date', 'end_time', 'is_overdue']


