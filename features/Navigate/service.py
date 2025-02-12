

# app/services/user_service.py
from features.Navigate.repository import CmdRepo
from features.Navigate.model import NavigateModel
from geopy.geocoders import Nominatim

class coordinatesService:
    def __init__(self, placename):
        self.place = placename
        self.coordinates = self.geocode_place()  # Call method immediately and store result

    def geocode_place(self):
        """
        Geocodes a place name to latitude and longitude using Nominatim.
        """
        geolocator = Nominatim(user_agent="my_geocoding_app")
        location = geolocator.geocode(self.place)

        if location:
            return (location.latitude, location.longitude)
        else:
            return None

            

class CommandService:

    def __init__(self,dest,cur):
        self.destination=dest
        self.current_loc=cur
        self.api_url=f"https://api.mapbox.com/directions/v5/mapbox/walking/{dest[1]}%2C{dest[0]}%3B{cur[0]}%2C{cur[1]}"

    def command(self) -> NavigateModel:

        print(self.api_url)

        cmdRepoInstance=CmdRepo(self.api_url)

        commands=cmdRepoInstance.GetCommands()

        print(commands)
        try:
            model=NavigateModel(self.destination,self.current_loc,commands[0])
        except:
            pass

        return model



#  77.7294485,11.3442867