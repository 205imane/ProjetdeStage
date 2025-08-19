from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, cin, nom, prenom, password=None, **extra_fields):
        if not cin:
            raise ValueError('Le CIN est obligatoire')
        if not nom:
            raise ValueError('Le nom est obligatoire')
        if not prenom:
            raise ValueError('Le prénom est obligatoire')
            
        user = self.model(
            cin=cin,
            nom=nom,
            prenom=prenom,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cin, nom, prenom, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            cin=cin,
            nom=nom,
            prenom=prenom,
            password=password,
            **extra_fields
        )

class User(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    cin = models.CharField(max_length=10, unique=True)
    division = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'cin'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"
       

    

class File(models.Model):
    fichier = models.FileField(upload_to='uploads/', default = "Fichier N'existe Pas")
    user = models.ForeignKey(User, on_delete=models.CASCADE , null = True )
    partage = models.BooleanField(default = False )
    shared_with = models.ManyToManyField(User, related_name="shared_files", blank = True)
    uploaded_at = models.DateField(null = True , blank = True)
    @property
    def __str__(self):
        return self.shared_with.exists()
    def __str__(self):
        return f"{self.fichier.name}"




