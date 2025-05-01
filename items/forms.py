# forms.py
from django import forms

class CheckoutForm(forms.Form):
    username = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    country = forms.CharField(max_length=100)
    note_to_lender = forms.CharField(widget=forms.Textarea)
