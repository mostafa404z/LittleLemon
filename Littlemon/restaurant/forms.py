from django.forms import ModelForm
from django.contrib.auth.models import User

class user(ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'email' , 'username' , 'password']