from PIL._tkinter_finder import tk
from numpy.f2py.crackfortran import analyzeargs_re_1

"""
from weatherexporter import WeatherExporter
from WeatherForecast import WeatherForecast
"""
import analyzer

from TitTacToe.TicTacToeGUI import TicTacToeGUI

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
"""
wf = WeatherForecast(
    latitude="35.68",
    longitude="139.69",
    startdate="2026-09-17",
    enddate="2026-09-24",
    city="Tokio",
)
wd = WeatherExporter(
    latitude="35.68",
    longitude="139.69",
    city="Tokio",
    startdate="2026-09-17",
    enddate="2026-09-24",
)

wf.visualize_weather_forecast()
wf.print_weather_forecast()
path=wd.export_to_csv()
"""


#zufall.zufallgame()
#print(zufall.addieren(1,2,3,4))
#tittac.spiel_brett(tittac.erstelle_brett())
#sportauto= Auto.SportAuto("ferrari","Poursche",2,"benzin","sport",50000)
#sportauto.display()
#sportauto.basedisplay()


#root = tk.Tk()
#app = TicTacToeGUI(root)
#root.mainloop()

#import tkinter
#print(tkinter.__file__)

#analyzer.Analyzer.open_file("C:\\Users\\farib\\PycharmProjects\\PythonProject\\sales-analysis\\output\\sales_data.json")
ana = analyzer.Analyzer("fcs","C:\\Users\\farib\\PycharmProjects\\PythonProject\\sales-analysis\\output\\nox.txt","txt")
ana.open_file()

