"""print("Hello World")
x="Hello World!!!"
print(x[6:11].count("o"))
print(x[6:11].count("W"))
print(x*2)
y=2
print("size:" + str(y.__sizeof__()))
print(x.find("World"))
index=x.find("World")
print(x[index:])
print(x.split(" "))"""
import request
import waehrungsrechner
import zufall
import tittac
import Auto
import requests
"""
y=int(input("bitte geben sie ein zahl ein: "))
y= y*2
print(y)
"""
#waehrungsrechner.waehrungsrechnen()

"""
a=1
if(a%2==0):
    print(a,"is divisible by 2")
else:
    print(a,"is divisible by 1")

list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
del list[0]
list.append(16)
list.remove(16)

for i in list:
    print(i)
print("extract value:",list.pop(2))
for i in list:
    print(i)

"""
"""
immutablelist=tuple([1,2,3,4]) #nicht veränderbar
print(immutablelist[0])
loopvariable= len(immutablelist)-1
print("loopvariable:",loopvariable)
for i in immutablelist:
    if(i%2==0):
        print(i,"is divisible by 2")


"""

"""
paris_tmp=request.get_weather(48.85,2.35)
london_tmp=request.get_weather(51.50,-0.12)
tokio_tmp=request.get_weather(35.68,139.69)
print(f"paris:{paris_tmp}C")

print(f"london:{london_tmp}C")
print(f"tokio:{tokio_tmp}C")
"""

data=request.get_weather_forecast_bytime()
request.extract_weather(data)
print("############################")
data= request.get_weather_forecast()
request.extract_weather(data)

#zufall.zufallgame()
#print(zufall.addieren(1,2,3,4))
#tittac.spiel_brett(tittac.erstelle_brett())
#sportauto= Auto.SportAuto("ferrari","Poursche",2,"benzin","sport",50000)
#sportauto.display()
#sportauto.basedisplay()

