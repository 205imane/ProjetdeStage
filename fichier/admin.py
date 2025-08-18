from django.contrib import admin
from .models import User , File
# Register your models here.

@admin.register(File)
class AdminFile(admin.ModelAdmin):
    list_display = ['fichier' , 'partage']
    list_filter = ['partage']