class Auto:
    def __init__(self, name,marke,sitze,energie,art):
        self.name = name
        self.marke = marke
        self.sitze = sitze
        self.energie = energie
        self.art = art
    def basedisplay(self):
        print(self.name,self.marke,self.sitze,self.energie,self.art)
class SportAuto(Auto):
    def __init__(self,name,marke,sitze,energie,art,preis):
        super().__init__(self,name,marke,sitze,energie,art)
        self.preis = preis
    def display(self):
        print(self.name,self.marke,self.sitze,self.energie,self.art,self.preis)
