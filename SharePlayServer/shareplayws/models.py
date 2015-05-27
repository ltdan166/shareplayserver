from django.db import models
from django.db.models.fields import AutoField
from geopy import Nominatim
from django.template.defaultfilters import default

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
    
    def __str__(self):
        return str(self.street_number) + " " + self.street_name + " " + self.city + " " + self.postal_code + " " + self.country    
    
class sp_person (models.Model):
    userid = models.CharField(max_length=10, primary_key=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=200)
    postal_address = models.ForeignKey(sp_address, null=True)
    
    def __str__(self):
        return self.firstname + " " + self.lastname    
    
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
    longitude = models.CharField(max_length=200, null=True)    
    latitude = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name + " : " + self.description    
    
    '''
    override the default saving method
    if the longitude/latitude is empty, calculate them with geopy
    '''
    def save (self, *args, **kwargs):
        if self.longitude == "" or self.latitude == "":
            geolocator = Nominatim ()
            full_add = self.street_number + " " + self.street_name + " " + self.city + " " + self.country
            location = geolocator.geocode (full_add)
            self.longitude = location.longitude()
            self.latitude = location.latitude()
        
    
class sp_event (models.Model):
    event_id = models.AutoField (primary_key=True)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(sp_person, related_name="created_by")
    event_date = models.DateTimeField('Event Date')
    location = models.ForeignKey(sp_location)
    is_public = models.BooleanField (default=False) #the created event is private for friends on ly or public for everyone
    player = models.ManyToManyField (sp_person, through='sp_player', through_fields=('event', 'player')) #the player list of each event

    def __str__(self):
        return self.name

class sp_player (models.Model):
    event = models.ForeignKey (sp_event)
    player = models.ForeignKey (sp_person, related_name="played_for")
    inviter = models.ForeignKey (sp_person, related_name="invited_by")
    invite_reason = models.CharField (max_length=300, null=True)
    
    def __str__(self):
        return self.player.firstname + " played for " + self.event.name
    
    