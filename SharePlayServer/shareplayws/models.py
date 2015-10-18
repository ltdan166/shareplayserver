from django.db import models
#from django.db.models.fields import AutoField
from geopy import Nominatim
#from django.template.defaultfilters import default
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save

# We create 4 models for the demo : person, event, location, address
    
class sp_address (models.Model): 
    ADD_TYPE = (
        ('H', 'Home'),
        ('W', 'Work')
    )   
    address_id = models.AutoField (primary_key=True)
    address_type = models.CharField (max_length=1, choices=ADD_TYPE, default="H")
    street_number = models.IntegerField ()
    street_name = models.CharField (max_length=200, null=True)
    city = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=5)
    country = models.CharField(max_length=100)
    longitude = models.FloatField(max_length=200, null=True, blank=True)    
    latitude = models.FloatField(max_length=200, null=True, blank=True)     
    
    def __str__(self):
        return str(self.street_number) + " " + self.street_name + " " + self.city + " " + self.postal_code + " " + self.country   
    
    '''
    override the default saving method
    if the longitude/latitude is empty, calculate them with geopy
    '''
    def save (self, *args, **kwargs):
        if self.longitude is None or self.latitude is None:
            geolocator = Nominatim ()
            full_add = str(self.street_number) + " " + self.street_name + " " + self.city + " " + self.country
            print (full_add)
            location = geolocator.geocode (full_add)
            if location is not None:
                self.longitude = location.longitude
                self.latitude = location.latitude
        super (sp_address, self).save (*args, **kwargs) 
    
class sp_person (models.Model):
    userid = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=50, null=True)
    profile = models.OneToOneField (User, null=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=200)
    postal_address = models.ForeignKey(sp_address, null=True)
    longitude = models.FloatField(max_length=200, null=True, blank=True)    
    latitude = models.FloatField(max_length=200, null=True, blank=True)
    last_know_long = models.FloatField(max_length=200, null=True, blank=True)
    last_know_lat = models.FloatField(max_length=200, null=True, blank=True)    
    
    def __str__(self):
        return self.firstname + " " + self.lastname
    
    '''
    override the default saving method
    if the longitude/latitude is empty, use the last known ones
    '''
    def save (self, *args, **kwargs):     
        if self.longitude is None or self.latitude is None:
            self.longitude = self.last_know_long
            self.latitude = self.last_know_lat
        else:
            self.last_know_long = self.longitude
            self.last_know_lat = self.latitude
        super (sp_person, self).save (*args, **kwargs)
        
def create_profile (sender, instance, created, **kwargs): 
    if created:
        #profile, created = sp_person.objects.get_or_create(profile=instance)
        Token.objects.create (user=instance)
        
post_save.connect(create_profile, sender=User)
    
class sp_location (models.Model):    
    location_id = models.AutoField (primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True)
    telephone = models.CharField(max_length=50, null=True)
    street_number = models.IntegerField (null=True)
    street_name = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    postal_code = models.CharField(max_length=5, null=True)
    country = models.CharField(max_length=100, null=True) 
    longitude = models.FloatField(max_length=200, null=True, blank=True)    
    latitude = models.FloatField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name + " : " + self.description    
    
    '''
    override the default saving method
    if the longitude/latitude is empty, calculate them with geopy
    '''
    def save (self, *args, **kwargs):
        geolocator = Nominatim ()
        full_add = str(self.street_number) + " " + self.street_name + " " + self.city + " " + self.country
        location = geolocator.geocode (full_add)
        if location is not None:
            self.longitude = location.longitude
            self.latitude = location.latitude
        else :
            self.longitude = 0
            self.latitude = 0
            
        print (full_add)
        super (sp_location, self).save (*args, **kwargs)
    
class sp_event (models.Model):
    event_id = models.AutoField (primary_key=True)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(sp_person, related_name="created_by")
    event_date = models.DateTimeField('Event Date')
    location = models.ForeignKey(sp_location)
    is_public = models.BooleanField (default=False) #the created event is private for friends on ly or public for everyone
    player = models.ManyToManyField (sp_person, through='sp_player', through_fields=('event', 'player')) #the player list of each event

    def __str__(self):
        return str(self.event_id) + " " + self.name

class sp_player (models.Model):
    event = models.ForeignKey (sp_event)
    player = models.ForeignKey (sp_person, related_name="played_for")
    inviter = models.ForeignKey (sp_person, related_name="invited_by")
    invite_reason = models.CharField (max_length=300, null=True)
    confirmed = models.BooleanField (default=False)
    
    def __str__(self):
        return self.player.firstname + " played for " + self.event.name
    
"""    
class sp_nearby_location (models.Model):
    person = models.ForeignKey (sp_person)
    location = models.ForeignKey (sp_location)
    address = models.ForeignKey (sp_address, null = True)
    distance = models.FloatField (max_length = 20, null = True)
    
    def __str__(self):
        return self.location.name + " is " + self.distance + " metres away from " + self.person.firstname
                    
    def getnearbylist (cls):
        locations = sp_location.object.all()
        gps_user = (self.person.latitude, self.person.longitude)
        nearby_loc_lst = []
        
        for each location, calculate the distance from user's one then return the list
        for location in locations:
            gps_loc = (location.latitude, location.longitude)
            dist = vincenty (gps_user, gps_loc).meters
            if dist <= distance:
                nearby_loc_lst.append(location)
        return nearby_loc_lst
           
"""    
    