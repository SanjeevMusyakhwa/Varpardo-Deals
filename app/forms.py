from django import forms
from .models import Order, Customer,User, Review  

class CheckoutForm(forms.ModelForm):
  ordered_by = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Ordered By'}))
  shipping_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Shipping Address'}))
  mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Mobile Number'}))
  email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email Address'}))
  class Meta:
    model = Order
    fields = ['ordered_by', 'shipping_address', 'mobile','email']

class CustomerRegisterForm(forms.ModelForm):
  username = forms.CharField(widget=forms.TextInput())
  email = forms.EmailField(widget=forms.EmailInput())
  password = forms.CharField(widget=forms.PasswordInput())
  address = forms.CharField(widget=forms.TextInput())
   
  class Meta:
    model = Customer
    fields =['username','full_name', 'email' ,'address', 'password']

  def clean_username(self):
    uname = self.cleaned_data.get('username')
    if User.objects.filter(username = uname).exists():
      raise forms.ValidationError("Customer With this username already exists.")
    return uname
  
class CustomerLoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput())
  password = forms.CharField(widget=forms.PasswordInput())


class AdminLoginForm(forms.Form):
  username = forms.CharField(widget=forms.TextInput())
  password = forms.CharField(widget=forms.PasswordInput())


