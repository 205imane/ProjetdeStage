from django.forms import ModelForm
from .models import User
from .models import File


class UserForm(ModelForm):
    class Meta :
        model = User
        fields = ['nom' , 'prenom' , 'cin' , 'division' , 'password']

class FileForm(ModelForm):
    class Meta :
        model = File
        fields = ['fichier' , 'partage']

