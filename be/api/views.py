from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# stats.nba.com API
from nba_api.stats.static import players

# Create your views here.
class Test(APIView):

    def get(self, request): 
        return Response("You have connected to the test endpoint successfully!") 


class MyFantasyRoster(APIView):

    def get(self, request):
        data = {
            "players": self.get_fantasy_roster(),            
        }

        return Response(data)
    
    def get_fantasy_roster(self):
        player_names = [ "Luka Doncic", "LeBron James", "Victor Wembanyama", "Desmond Bane", "Alperen Sengun", "Austin Reaves", "Klay Thompson", "Spencer Dinwiddie", "Daniel Gafford", "Malcolm Brogdon", "Caris LeVert", "Bennedict Mathurin", "Saddiq Bey",]
        
        return player_names
    