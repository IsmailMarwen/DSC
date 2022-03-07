from asyncio.windows_events import NULL
from distutils.command.upload import upload
from operator import index
from pyexpat import model
from re import A
from statistics import mode
from django.db import models
class Partner(models.Model):
    idPartner=models.AutoField(primary_key=True,unique=True,blank=True)
    name=models.CharField(max_length=20)
    logo=models.ImageField(upload_to="images/partenaire/")
    def __str__(self):
        return self.name
class Admin(models.Model):
    idAdmin=models.AutoField(primary_key=True,unique=True,blank=True)
    partner=models.ForeignKey(Partner, on_delete=models.CASCADE)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    image=models.ImageField(upload_to="images/admins/")
    def __str__(self):
        return self.username

class Video(models.Model):
    idVideo=models.AutoField(primary_key=True,unique=True,blank=True)
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE)
    categorie=models.CharField(max_length=50)
    vd=models.FileField(upload_to="videos/")
    minAge=models.IntegerField()
    maxAge=models.IntegerField()
    homme=models.BooleanField()
    femme=models.BooleanField()
    def __str__(self):
        return self.categorie
class Playlist(models.Model):
    idPlaylist=models.AutoField(primary_key=True,unique=True,blank=True)
    video = models.ManyToManyField(Video)
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE)
    libelle=models.CharField(max_length=50)
    def __str__(self):
        return self.libelle
class Ecran(models.Model):
    idEcran=models.CharField(max_length=50)
    idDevice=models.CharField(max_length=50)
    nameDevice=models.CharField(max_length=30)
    timeOpen=models.DateTimeField(blank=True)
    partner=models.ForeignKey(Partner,on_delete=models.CASCADE) 
    def __str__(self):
        return self.idEcran
class VideoEcran(models.Model):
    statut=models.BooleanField(default=False)
    partner=models.ForeignKey(Partner,on_delete=models.CASCADE) 
    video=models.CharField(max_length=2000)
    temps=models.CharField(max_length=50) 
    index=models.IntegerField(default=0)
