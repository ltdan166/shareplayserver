from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from shareplayws import views
from rest_framework import authtoken
import shareplayws

urlpatterns = [
    # Examples:
    # url(r'^$', 'Demo_SharePlay.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url for admin page
    url(r'^admin/', include(admin.site.urls)),
    
    
    #enable rest login
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
     #url for address rest api
    #addresses list
    url(r'^addresses/$', shareplayws.views.AddressList.as_view()),
    
    #person detail
    url(r'^address/(?P<pk>[0-9]+)/$', shareplayws.views.AddressDetail.as_view()),
    
    #url for person rest api
    #persons list
    url(r'^persons/$', shareplayws.views.PersonList.as_view()),
    
    #person detail
    url(r'^person/(?P<pk>[0-9]+)/$', shareplayws.views.PersonDetail.as_view()),
    
    #url for event rest api
    #events list
    url(r'^events/$', shareplayws.views.EventList.as_view()),
    
    #event detail
    url(r'^event/(?P<pk>[0-9]+)/$', shareplayws.views.EventDetail.as_view()),
    
    #url for location rest api
    #locations list
    url(r'^locations/$', shareplayws.views.LocationList.as_view()),
    
    #location detail
    url(r'^location/(?P<pk>[0-9]+)/$', shareplayws.views.LocationDetail.as_view()),
    
    #url for player rest api
    #player list
    url(r'^players/$', shareplayws.views.PlayerList.as_view()),
    
    #location detail
    #url(r'^player/(?P<pk>[0-9]+)/$', views.PlayerDetail.as_view()),
    
    #url for nearby location rest api
    #nearby location list  
    url(r'^nearby$', shareplayws.views.NearbyLocationList.as_view()),
    
    url(r'^api-token-auth/', authtoken.views.obtain_auth_token),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
