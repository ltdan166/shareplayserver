'''
Created on Apr 22, 2015

@author: dan
'''
from rest_framework import serializers
from shareplayws.models import sp_person, sp_event, sp_location, sp_address, sp_player
from django.core.exceptions import ObjectDoesNotExist
from django.views.i18n import null_javascript_catalog

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = sp_address
        fields = ('address_id', 'address_type', 'street_number', 'street_name', 'city', 'postal_code', 'country', 'latitude', 'longitude')

class PersonSerializer(serializers.ModelSerializer):
    postal_address = AddressSerializer()
    
    class Meta:
        model = sp_person
        fields = ('userid', 'firstname', 'lastname', 'email', 'telephone', 'postal_address')
        depth = 1
        
        
class PersonSerializerPOST (serializers.ModelSerializer):  
    userid = serializers.CharField (max_length=10)
    firstname = serializers.CharField (max_length=200)
    lastname = serializers.CharField (max_length=200)
    email = serializers.CharField (max_length=200)
    telephone = serializers.CharField (max_length=20)
    postal_address = AddressSerializer()
    
    class Meta:
        model = sp_person        
        fields = ('userid', 'firstname', 'lastname', 'email', 'telephone', 'postal_address')
        depth = 1
     
    def create (self, validated_data):
        #take out the address data and create an address record with them        
        address_data = validated_data.pop('postal_address')   
        postal_address = sp_address (address_type = address_data['address_type'], street_number = address_data['street_number'], street_name = address_data['street_name'], city = address_data['city'], postal_code=address_data['postal_code'], country=address_data['country'] )
        postal_address.save ()
        
        #create a person with address
        person = sp_person (userid = validated_data['userid'], firstname = validated_data['firstname'], lastname = validated_data['lastname'], email=validated_data['email'], telephone=validated_data['telephone'], postal_address=postal_address)
        person.save ()
        return person
         
class LocationSerializer (serializers.ModelSerializer):
    class Meta:
        model = sp_location
        fields = ('location_id', 'name', 'description', 'email', 'telephone', 'street_number', 'street_name', 'postal_code', 'city', 'country', 'longitude', 'latitude')
        
class EventSerializerPOST (serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    owner = serializers.CharField(max_length=200)
    event_date = serializers.DateTimeField()
    location = serializers.CharField(max_length=200)            
    
    
    class Meta:
        model = sp_event
        fields = ('event_id', 'name', 'owner', 'event_date', 'location')
        depth = 1
        
    def create (self, validated_data):
        try:                        
            owner = sp_person.objects.get(userid=validated_data['owner'])            
            location = sp_location.objects.get (location_id=validated_data['location'])
            event = sp_event (name=validated_data['name'], owner=owner, event_date=validated_data['event_date'],location=location)
            event.save()
            return event                 
        except ObjectDoesNotExist:
            raise serializers.ValidationError()
                     
class EventSerializerGET (serializers.ModelSerializer):    
    name = serializers.CharField(max_length=200)    
    owner = PersonSerializer ()
    event_date = serializers.DateTimeField()
    location = LocationSerializer()                
    
    
    class Meta:
        model = sp_event
        fields = ('event_id', 'name', 'owner', 'event_date', 'location', 'player')
        depth = 1        
          
class PlayerSerializerPOST (serializers.ModelSerializer):
    event = serializers.CharField(max_length=200)
    player = serializers.CharField(max_length=200)
    inviter = serializers.CharField(max_length=200)
    invite_reason = serializers.CharField(max_length=300)
        
    class Meta:
        model = sp_player
        fields = ('event', 'player', 'inviter', 'invite_reason')
        depth = 1
        
    def create (self, validated_data):
        try:                        
            #get player
            player_person = sp_person.objects.get(userid=validated_data['player'])            
            
            #get event
            event = sp_event.objects.get (event_id=validated_data['event'])
            
            #get inviter if populated
            #if validated_data['inviter'] != '' :
            inviter = sp_person.objects.get(userid=validated_data['inviter'])
            
            player = sp_player (event=event, player=player_person, inviter=inviter, invite_reason=validated_data['invite_reason'])
            player.save()
            return player                 
        except ObjectDoesNotExist:
            raise serializers.ValidationError()
        
class PlayerSerializerGET (serializers.ModelSerializer):
    '''
    event = EventSerializerGET ()
    player = PersonSerializer ()
    inviter = PersonSerializer ()
    invite_reason = serializers.CharField(max_length=300)            
    '''
    
    class Meta:
        model = sp_player
        fields = ('event', 'player', 'inviter', 'invite_reason')
        #depth = 1                        