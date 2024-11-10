from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
  ordered_by = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Ordered By'}))
  shipping_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Shipping Address'}))
  mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Mobile Number'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email Address'}))
  class Meta:
    model = Order
    fields = ['ordered_by', 'shipping_address', 'mobile','email']