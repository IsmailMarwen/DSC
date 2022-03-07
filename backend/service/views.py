from base64 import b64decode
from email.message import Message
from turtle import home
from PIL import Image
import numpy as np
import io
import base64
import imghdr
from django.core.files.base import ContentFile   
from io import BytesIO
from asyncio.windows_events import NULL
from email.mime import application, image
from http import client
from re import A, T, X

from torch import t
from .models import *
import json
from unicodedata import numeric
from xml.etree.ElementTree import XML
from django.shortcuts import render
import cv2
from django.core import serializers
from django.http import HttpResponse,HttpResponseForbidden,JsonResponse
import speech_recognition as sr
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.db.models import Q
import os
from django.conf import settings
from rest_framework.decorators import api_view
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import string
import random
import json
from django.shortcuts import get_object_or_404
dict={}
dash={}


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def getPlaylist( admin):
    try:
        return Playlist.objects.filter(admin=admin)
    except Playlist.DoesNotExist:
        return False
@api_view(['GET'])
def getPlaylistForPartner(request,id):
    playlist=[]
    partner=Partner.objects.get(idPartner=id)
    admins=Admin.objects.filter(partner=partner)
    for i in admins:
        p=getPlaylist(i).values()
        playlist.append(list(p))
    print(playlist)
    data=json.dumps({"playlists":playlist})
    
    return HttpResponse(data, content_type="application/json")
@api_view(['GET'])
def getPlaylistAdmin(request,id):

    admin=Admin.objects.get(idAdmin=id)
    playlist=getPlaylist(admin).values() 
    data=json.dumps({"playlists":list(playlist)})
    return HttpResponse(data, content_type="application/json")
@api_view(['GET'])
def getPartner(request,id):
    admin=Admin.objects.get(idAdmin=id)
    partnerName=admin.partner.name
    partnerLogo=admin.partner.logo.url
    data=json.dumps({"partnerName":partnerName,"partnerLogo":"http://127.0.0.1:8000"+partnerLogo})
    return HttpResponse(data, content_type="application/json")
@api_view(['GET'])
def getVideosPlaylist(request,id):
    data={}
    playlist=Playlist.objects.get(idPlaylist=id)
    data=json.dumps({"videos":list(playlist.video.all().values())})
    return HttpResponse(data, content_type="application/json")
@api_view(['POST'])
def addEcran(request):
    idEcran=id_generator()
    idPartner=request.data['idPartner']
    idDevice=request.data['idDevice']
    nameDevice=request.data['nameDevice']
    playlist=[]
    partner=Partner.objects.get(idPartner=idPartner)
    try:
        ecran=Ecran.objects.get(idDevice=idDevice)
    except Ecran.DoesNotExist:    
        ecran=Ecran(idEcran=idEcran,partner=partner,idDevice=idDevice,nameDevice=nameDevice)
        ecran.save()
    admins=Admin.objects.filter(partner=partner)
    for i in admins:
        p=getPlaylist(i).values()
        playlist.append(list(p))
    data=json.dumps({"playlists":playlist,"idEcran":idEcran})
    return HttpResponse(data, content_type="application/json")
@api_view(['GET'])
def getAllPartner(request):
   data ={}
   partners=list(Partner.objects.values())
   data['partners']=partners
   print(data)
   return JsonResponse(data)
@api_view(['POST'])
def Login(request):
    data=request.data
    username=data['username']
    password=data['password']
    session =""
    try:
        admin=Admin.objects.get(username=username,password=password) 
        session=json.dumps({'connect':True,'message':'connect avec succes','image':"http://127.0.0.1:8000"+admin.image.url,'id':admin.idAdmin})
    except Admin.DoesNotExist:
        session=json.dumps({'connect':'false','message':'Invalid User Or Password'})
    return HttpResponse(session, content_type="application/json")
@api_view(['GET'])
def getUser(request,username):
    admin=Admin.objects.get(username=username)
    print(admin)
    data=json.dumps({'user':'none'})
    return HttpResponse(data, content_type="application/json")
@api_view(['POST'])
def addPlaylist(request):
    data=""
    idAdmin=request.data['idAdmin']
    admin=Admin.objects.get(idAdmin=idAdmin)
    libelle=request.data['libelle']
    playlist=Playlist.objects.create(admin=admin,libelle=libelle)
    for i in request.data['chose']:
        video=Video.objects.get(idVideo=i)
        playlist.video.add(video)
   
    data=json.dumps({'message':'New playlist'})
    return HttpResponse(data, content_type="application/json")
@api_view(['POST'])
def addVideo(request):
    idAdmin=request.data['idAdmin']
    homme=request.data['homme']
    femme=request.data['femme']
    minAge=int(request.data['minAge'])
    maxAge=int(request.data['maxAge'])
    admin=Admin.objects.get(idAdmin=idAdmin)
    categorie=request.data['categorie']
    vd=request.data['vd'] 
    format, vdstr = vd.split(';base64,') 
    ext = format.split('/')[-1] 
    v=ContentFile(base64.b64decode(vdstr), name=categorie+'.' + ext)
    video=Video(admin=admin,categorie=categorie,vd=v,homme=homme,femme=femme,minAge=minAge,maxAge=maxAge)
    video.save()
    data=json.dumps({"added":"yes"})
    return HttpResponse(data,content_type="application/json")
@api_view(['POST'])
def updateVideo(request,id):
    partner=Partner.objects.get(idPartner=id)
    timeVd=request.data['timeVd']
    index=request.data['index']
    idA=request.data['idAdmin']
    vid=request.data['vd']
    data=json.dumps({"vd":vid,"timeVd":timeVd})
    dict[id]={"vd":vid,"timeVd":timeVd,'stat':True,'index':index,'idA':idA}
    return HttpResponse(data,content_type="application/json")
@api_view(['GET'])
def getTimeVideo(request,id):
    if(len(dict)>0):
        try:
          data=json.dumps(dict[id])
        except KeyError:
          data=json.dumps({'stat':False})
    else:
        data=json.dumps({'stat':False})
    
    return HttpResponse(data,content_type="application/json")
@api_view(['GET'])
def reloadTime(request,id):
    if(len(dict)>0):
        try:
          dict.pop(id)
          data=json.dumps({'stat':False})
        except KeyError:
          data=json.dumps({'stat':False})
    else:
        data=json.dumps({'stat':False})
    
    return HttpResponse(data,content_type="application/json")    
  
@api_view(['GET'])
def getAdminVd(request,id):
    data=''
    try:
       vd=Video.objects.get(idVideo=id)
       data=json.dumps({'idAdmin':vd.playlist.admin.idAdmin,'username':vd.playlist.admin.username})
       
    except Video.DoesNotExist:
        data=json.dumps({'video':'not exist'})
    return HttpResponse(data,content_type="application/json")
@api_view(['POST'])
def getVideoEcran(request,id):
      ecrans=[]
      admin=Admin.objects.get(idAdmin=id)
      ecran=request.data['ecran']
      vd=request.data['vd']
      data=json.dumps({'admin':admin.username,'ecran':ecran,'video':vd})
      ecrans+=[(ecran,vd)]
      for  v in ecrans:
         dash[id]=v
      print(data)
      return HttpResponse(data,content_type="application/json")
def getDetail(id):
    return dash[id]
@api_view(['GET'])
def dashbord(request,id):
    admin=Admin.objects.get(idAdmin=id)
    nbv=0
    partnerName=admin.partner.name
    playlist=getPlaylist(admin).values() 
    p=getPlaylist(admin)
    nbPlaylist=len(list(playlist))
    for i in p:
        print(i)
        videos=Video.objects.filter(playlist=i)
        print(videos)
        for j in videos:
            nbv=nbv+1
    print(nbv)
    data=json.dumps(dash[id])
    return HttpResponse(data,content_type="application/json") 
@api_view(['POST'])
def addVideoEcran(request):
    idPartner=request.data['idPartner']
    vd=request.data['vd']
    temps=request.data['temps']
    index=request.data['index']
    partner=Partner.objects.get(idPartner=idPartner)
    vdEcran=VideoEcran.objects.get(partner=partner)
    vdEcran.video=vd
    vdEcran.temps=temps
    vdEcran.index=index
    vdEcran.statut=True
    vdEcran.save()
    data=json.dumps({'updated':True})
    return HttpResponse(data,content_type='application/json')
@api_view(['GET'])
def getVideoEcrans(request,id):
    partner=Partner.objects.get(idPartner=id)
    vdEcran=VideoEcran.objects.get(partner=partner)
    data=json.dumps({'vd':vdEcran.video,'temps':vdEcran.temps,'statut':vdEcran.statut,'index':vdEcran.index})
    return HttpResponse(data,content_type='application/json')
@api_view(['POST'])
def resetVideoEcrans(request,id):
    vd=request.data['vd']
    temps=request.data['temps']
    index=request.data['index']
    partner=Partner.objects.get(idPartner=id)
    vdEcran=VideoEcran.objects.get(partner=partner)
    vdEcran.video=vd
    vdEcran.temps=temps
    vdEcran.index=index
    vdEcran.statut=True
    vdEcran.save()
    data=json.dumps({'updated':True})
    return HttpResponse(data,content_type='application/json')
@api_view(['POST'])
def addMsg(request,msg):
    message=Message(msg=msg)
    message.save()
    data=json.dumps({'added':True})
    return HttpResponse(data,content_type='application/json')
@api_view(['GET'])
def getAllMessages(request):
   data ={}
   messages=list(Message.objects.values())
   data['messages']=messages
   print(data)
   return JsonResponse(data)
@api_view(['GET'])
def getVideoAdmin(request,id):
    admin=Admin.objects.get(idAdmin=id)
    video=(Video.objects.filter(admin=admin).values())
    print(list(video))
    data=json.dumps({'videos':list(video)})
    return HttpResponse(data,content_type='application/json')