def erstelle_brett():
    brett=[]
    for i in range(3):
        zeile=[" "," "," "]
        brett.append(zeile)
    return brett
def druck_brett(brett):
    for zeile in brett:
        print("|".join(zeile))
        print("------")
def check_remie(brett):
    for zeile in brett:
        if " " in zeile:
            return False

    return True

def spiel_brett(brett):
    brett= erstelle_brett()
    aktuelle_spieler="X"
    while True:
        druck_brett(brett)
        zeile= int(input(f"spieler {aktuelle_spieler}, wähle deine zeile 0-2 "))
        spalte = int(input(f"spieler {aktuelle_spieler}, wähle deine spalte 0-2 "))
        if not spiel_zug(brett,zeile, spalte,aktuelle_spieler):
            print("Not allow")
            continue

        if check_winner(brett,aktuelle_spieler):
            druck_brett(brett)
            print(f"spieler {aktuelle_spieler} won the game")
            break
        elif check_remie(brett):
            druck_brett(brett)
            print(f"Remie")
            break
        aktuelle_spieler = "O" if aktuelle_spieler == "X" else "X"

def spiel_zug(brett, zeile, spalte, spieler):
    if brett[zeile][spalte] == " ":
        brett[zeile][spalte] = spieler
        return True
    else:
        return False
def check_winner(brett,spieler):
    for zeile in range(3):
        if brett[zeile][0] == brett[zeile][1] == brett[zeile][2] == spieler:
            return True
    for spalte in range(3):
        if brett[0][spalte] == brett[1][spalte] == brett[2][spalte] == spieler:
            return True
    if (brett[0][0] == brett[1][1] == brett[2][2] == spieler or
            brett[2][0] == brett[1][1] == brett[2][0] == spieler):
        return True