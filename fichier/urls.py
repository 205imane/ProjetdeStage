from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Index, Nouveau_fichier, Remplacer_fichier, Fichier_disponible ,Sign_up,Welcome,Ajouter_avecsuc,Logout, Se_connecter


name = "fichier"
urlpatterns= [

    path('index/',Index.as_view(),name ='index'),
    path('signup/',Sign_up.as_view(),name='signup'),
    path('seconnecter/',Se_connecter.as_view(),name='seconnecter'),
    path('welcome/',Welcome.as_view(),name='welcome'),
    path('nouveauFichier/',Nouveau_fichier.as_view(),name = 'nouveauFichier'),
    path('logout/',Logout.as_view(),name = 'logout'),
    path('ajouteavecsuc/',Ajouter_avecsuc.as_view(),name='ajouterAvecsuc'),
    path('remplacerFichier/<int:file_id>/',Remplacer_fichier.as_view(),name = 'remplacerFichier'),
    path('fichierDisponible/',Fichier_disponible.as_view(),name= 'fichierDisponible'),
]

if settings.DEBUG :

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)