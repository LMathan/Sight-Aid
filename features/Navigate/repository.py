import requests

# Data Source Class
class CmdRepo:
    def __init__(self, api_url:str):

        self.api_url = api_url
        self.params = {
                        "alternatives": "true",
                        "continue_straight": "true",
                        "geometries": "geojson",
                        "language": "en",
                        "overview": "full",
                        "steps": "true",
                        "access_token": "pk.eyJ1IjoibWF0aGFuMzAwNyIsImEiOiJjbTZ5bjB4eHUwenM0MnFzaXo0b2R6M3ZkIn0.4umFWVz3OHuzBcRvf451VA" 
                    }


    def GetCommands(self):

        response = requests.get(self.api_url, params=self.params)

        if response.status_code == 200:
            data = response.json()
            
            instructions = [
                            step["maneuver"]["instruction"]
                            for route in data["routes"]
                            for leg in route["legs"]
                            for step in leg["steps"]
                            ]

        return instructions


