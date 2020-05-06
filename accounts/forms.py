from django.forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class createOrder(ModelForm):
    class Meta:
        model = Order
        fields= '__all__'

class createCustomer(ModelForm):
    class Meta:
        model = Customer
        fields= '__all__'

class createProduct(ModelForm):
    class Meta:
        model = Product
        fields= '__all__'

class createOrderHistory(ModelForm):
    class Meta:
        model = OrderHistory
        fields= '__all__'

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']