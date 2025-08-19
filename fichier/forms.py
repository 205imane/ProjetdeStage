from django.forms import ModelForm
from .models import User
from .models import File
from django import forms


class UserForm(ModelForm):
    class Meta :
        model = User
        fields = ['nom' , 'prenom' , 'cin' , 'division' , 'password']

class FileForm(ModelForm):
    cin = forms.CharField(required=False, label = "CIN de l'utilisateur")
    class Meta :
        model = File
        fields = ['fichier' , 'partage', 'cin']

