from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
 path('getPlaylistPartner/<id>/',views.getPlaylistForPartner,name="getPlaylistPartner"),
 path('getPlaylistAdmin/<id>/',views.getPlaylistAdmin,name="getPlaylistAdmin"),
 path('getPartner/<id>/',views.getPartner,name='getPartner'),
 path('getVideos/<id>/',views.getVideosPlaylist,name='getVideo'),
 path('newEcran/',views.addEcran,name='newEcran'),
 path('getPartners/',views.getAllPartner,name='getPartners'),
 path('login/',views.Login,name='login'),
 path('getUser/<username>',views.getUser,name='getuser'),
 path('addPlaylist/',views.addPlaylist,name='addPlaylist'),
 path('addVideo/',views.addVideo,name='addVideo'),
 path('updateVideo/<id>/',views.updateVideo,name='updateVideo'),
 path('getTimeVideo/<id>/',views.getTimeVideo,name='getTimeVideo'),
 path('reloadTime/<id>/',views.reloadTime,name='reloadTime'),
 path('dashbord/<id>/',views.dashbord,name='dashbord'),
 path('getAdminVd/<id>/',views.getAdminVd,name='getAdminVd'),
 path('getVideoEcran/<id>/',views.getVideoEcran,name='getVideoEcran'),
 path('addVideoEcran/',views.addVideoEcran,name='addVideoEcarn'),
 path('getVideoEcrans/<id>/',views.getVideoEcrans,name='getVideoEcrans'),
 path('resetVideoEcrans/<id>/',views.resetVideoEcrans,name='resetVideoEcrans'),
 path('getAllMessages/',views.getAllMessages,name='getAllMessages'),
  path('addMsg/<msg>/',views.addMsg,name='addMsg'),
  path('getVideoAdmin/<id>/',views.getVideoAdmin,name='getVideoAdmin')
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
