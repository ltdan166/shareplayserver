from django.http import HttpResponse 
from rest_framework import status
from rest_framework.response import Response
from shareplayws.models import sp_event, sp_person, sp_location, sp_address, sp_player
from shareplayws.serializers import PersonSerializer, PersonSerializerPOST, EventSerializerPOST, EventSerializerGET, LocationSerializer, AddressSerializer, PlayerSerializerPOST, PlayerSerializerGET
from rest_framework.views import APIView
from rest_framework import generics
from geopy.distance import vincenty
from piston_mini_client.failhandlers import NoneFailHandler


class PersonList(APIView):
    """
    List all or create new person 
    """        
    
    def get (self, request, format=None):        
        person = sp_person.objects.all()
        serializer = PersonSerializer(person, many = True)
        return Response(serializer.data)
        
    def post (self, request, format=None):
        serializer = PersonSerializerPOST(data=request.data)
        if serializer.is_valid():            
            serializer.save()     
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.data, status=status.HTTP_400_BAD_REQUEST)  
          

class PersonDetail(APIView):
    """
    Retrieve, update or delete a person instance 
    """        

    def get_object (self, pk):          
    #try to find the person with the pk, if not found, return an error
        try:
            return sp_person.objects.get(pk=pk)
        except sp_person.DoesNotExist:
            return Response (status=status.HTTP_404_NOT_FOUND)
    
    #return the person with the pk
    def get(self, request, pk, format=None):
        person = self.get_object(pk)        
        serializer = PersonSerializer (person)
        return Response(serializer.data)
        
    #update the person
    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer (person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete the persons
    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
       
class EventList (APIView):
    """
    List all or create new event 
    """
       
    def get (self, request, format=None):
    #list of all event or create new event
        event = sp_event.objects.all()
        serializer = EventSerializerGET(event, many = True)
        return Response(serializer.data)
        
    def post (self, request, format=None):            
        serializer = EventSerializerPOST(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)        

class EventDetail (APIView):
    """
    Retrieve, update, delete an event
    """
    
    #try to find the person with the pk, if not found, return an error
    def get_object (self, pk):
        try:
            event = sp_event.objects.get(event_id=pk)
            return event
        except sp_event.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)            
    
    #if method is GET, return the event with the pk
    def get (self, request, pk, format=None):    
        event = self.get_object(pk)
        serializer = EventSerializerGET (event)
        return Response(serializer.data)
    
    #if method is PUT, try to update the event
    def put (self, request, pk, format=None):    
        event = self.get_object(pk)
        serializer = EventSerializerPOST (event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete the event
    def delete (self, request, pk, format=None):
        event = self.get_object(pk)     
        event.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)        


class LocationList (APIView):
    """
    List of all locations or create new location
    """
    
    def get (self, request, format=None):    
        location = sp_location.objects.all()
        serializer = LocationSerializer(location, many = True)
        return Response(serializer.data)
        
    def post (self, request, format=None): 
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response (serializer.data, status=status.HTTP_400_BAD_REQUEST)  
    
class LocationDetail (APIView):
    """
    Retrieve, update, delete a location
    """
    
    #try to find the locations with the pk, if not found, return an error
    def get_object (self, pk):
        try:
            return sp_location.objects.get(pk=pk)
        except sp_location.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    
    #return the location with pk
    def get (self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer (location)
        return Response(serializer.data)
    
    #update the location
    def put (self, request, pk, format=None):        
        location = self.get_object(pk)
        serializer = LocationSerializer (location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete (self, request, pk, format=None):
        location = self.get_object(pk)
        location.delete()
        return Response (status=status.HTTP_204_NO_CONTENT)
    
class PlayerList (APIView):
    """
    List all or create new event 
    """
       
    def get (self, request, format=None):
    #list of all event or create new event
        player = sp_player.objects.all()
        serializer = PlayerSerializerGET(player, many = True)
        return Response(serializer.data)
        
    def post (self, request, format=None):            
        serializer = PlayerSerializerPOST(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)      
    
class AddressList (generics.ListCreateAPIView):
    """
    List of all address or create new address
    """
    queryset = sp_address.objects.all()
    serializer_class = AddressSerializer
    
class AddressDetail (generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or Delete an address
    """
    queryset = sp_address.objects.all()
    serializer_class = AddressSerializer

class NearbyLocationList (generics.ListAPIView):
    """
    Retrieve the list of nearby locations for user
    """
    serializer_class = LocationSerializer    
    
    def get_queryset (self):        
        locations = sp_location.objects.all()
        locations_list = list (locations)
        long = self.request.query_params.get ('long', None)
        lat = self.request.query_params.get ('lat', None)
        distance = self.request.query_params.get ('distance', None)
        if distance is None:
            distance = 5000 
                
        #Debug information on actual user's location        
        print ('Actual User''s Location : ')        
        print ('lat :' + lat + ' long : ' + long + ' distance : ' + str(distance))
        print ('----------------------------------')
        #end debug    
        
        if long is not None and lat is not None and distance is not None:
            gps_user = (lat, long)
            nearby_loc_lst = []
            
            """for each location, calculate the distance from user's one then return the list"""
            for location in locations_list:
                gps_loc = (location.latitude, location.longitude)                
                dist = vincenty (gps_user, gps_loc).meters
                
                #debug information on location 
                print ('----------------------------------')
                print (location)
                print ('lat :' + location.latitude + ' long : ' + location.longitude) 
                print ('Distance : ' + str(dist))
                print ('----------------------------------')
                #end debug
                
                if dist <= float(distance):
                    nearby_loc_lst.append(location)
                    
            if nearby_loc_lst.__sizeof__() > 0:
                serializer = LocationSerializer (nearby_loc_lst)
                return nearby_loc_lst
        return None
            