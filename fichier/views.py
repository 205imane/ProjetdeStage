from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from fichier.forms import UserForm, FileForm
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import File
from django.http import Http404
from django.db.utils import IntegrityError

# Use the custom user model
User = get_user_model()


class Index(View):
    template_name = "fichier/index.html"

    def get(self, request):
        return render(request, self.template_name)


from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()

class Se_connecter(View):
    template_name = 'fichier/seconnecter.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        cin = request.POST.get('cin')
        password = request.POST.get('password')
        user = authenticate(request, cin=cin, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            # Check if CIN exists
            if not User.objects.filter(cin=cin).exists():
                messages.error(request, "CIN introuvable. Veuillez vous inscrire.")
                return redirect('signup')
            else:
                messages.error(request, "Mot de passe incorrect.")
            return redirect('seconnecter')


class Nouveau_fichier(View):
    template_name = 'fichier/nouveau_fichier.html'

    def get(self, request):
        form = FileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FileForm(request.POST, request.FILES)
        print('form is valid ?', form.is_valid())
        if form.is_valid():
            fichier = form.save(commit=False)
            fichier.user = request.user 
            fichier.save()
            print('saved file :', fichier.fichier.name)
            return redirect('ajouterAvecsuc')
        return render(request, self.template_name, {'form': form})


class Remplacer_fichier(View):
    template_name = 'fichier/remplacer_fichier.html'

    def get(self, request, file_id):
        fichier = get_object_or_404(File, id=file_id, user=request.user)
        return render(request, self.template_name, {'fichier': fichier})

    def post(self, request, file_id):
        fichier = get_object_or_404(File, id=file_id, user=request.user)
        nouveau_fichier = request.FILES.get('fichier')

        if nouveau_fichier:
            if fichier.fichier:
                fichier.fichier.delete(save=False)
            fichier.fichier = nouveau_fichier
            fichier.save()
            messages.success(request, "Le fichier a été remplacé avec succès !")
            return redirect('fichierDisponible')
        else:
            messages.error(request, "Veuillez sélectionner un fichier pour le remplacement.")
            return render(request, self.template_name, {'fichier': fichier})


class Fichier_disponible(View):
    template_name = 'fichier/fichier_disponible.html'

    def get(self, request):
        if not request.user.is_authenticated:
            raise Http404("Page Not Found")

        files = File.objects.filter(user=request.user)
        return render(request, self.template_name, {'files': files})


class Sign_up(View):
    template_name = "fichier/signUp.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        cin = request.POST.get("cin")
        division = request.POST.get("division")
        password = request.POST.get("password")

        if not all([nom, prenom, cin, password]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return redirect('signup')

        try:
            user = User.objects.create_user(
                cin=cin,
                password=password,
                nom=nom,
                prenom=prenom,
                division=division
            )
            user = authenticate(request, username=cin, password=password)
            if user is not None:
                login(request, user)
                return redirect('welcome')
        except IntegrityError:
            messages.error(request, "Un utilisateur avec ce CIN existe déjà.")
            return redirect('signup')
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {str(e)}")
            return redirect('signup')


class Welcome(View):
    template_name = 'fichier/welcome.html'
    files = File.objects.all()

    def get(self, request):
        return render(request, self.template_name)


class Ajouter_avecsuc(View):
    template_name = "fichier/ajouteravecsuc.html"

    def get(self, request):
        return render(request, self.template_name)


class Logout(View):
    template_name = "fichier/logout.html"

    def get(self, request):
        logout(request)
        return redirect('index')
