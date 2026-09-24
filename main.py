
import request
import waehrungsrechner
import zufall
import tittac
import Auto
import requests
from WeatherForecast import WeatherForecast


"""
paris:
    latitude="48.85"
    longitude="2.35"
london:
    latitude="31.50"
    longitude="-0.12" 
tokio:
    latitude="35.68"
    longitude="139.69"

"""

wf = WeatherForecast(
    latitude="35.68",
    longitude="139.69",
    startdate="2026-09-17",
    enddate="2026-09-24",
    city="Tokio",
)


wf.visualize_weather_forecast()
wf.print_weather_forecast()
#zufall.zufallgame()
#print(zufall.addieren(1,2,3,4))
#tittac.spiel_brett(tittac.erstelle_brett())
#sportauto= Auto.SportAuto("ferrari","Poursche",2,"benzin","sport",50000)
#sportauto.display()
#sportauto.basedisplay()

