#Kortit
from audioop import reverse
from random import shuffle as sekoita

class Kortti:
    def __init__(self, arvo: int, maa: str):
        self.arvo = arvo
        self.maa = maa

    def __str__(self):
        return f"{self.maa} {self.arvo}"

class Pakka:
    def __init__(self):
        self.pakka = []
    
    def kasaa(self):
        maat = ["Hertta", "Ruutu", "Pata", "Risti"]
        for maa in maat:
            for n in range(1, 14):
                kortti = Kortti(n, maa)
                self.pakka.append(kortti)
    
    def sekoita(self):
        sekoita(self.pakka)
    
    #jakaa päällimmän
    def jaa(self):
        kortti = self.pakka[-1]
        self.pakka.remove(kortti)
        return kortti

class Pelaaja:
    def __init__(self, nimi: str):
        self.name = nimi
        self.hand = []

#
# Pakka toimii ??
#

def make_a_table(n: int):
    # loop for making players
    pelaajat = []
    for i in range(n):
        nimi = input("nimi:")
        player = Pelaaja(nimi)
        pelaajat.append(player)
    return pelaajat

# Käsi

def hand(pelaajat: list, pakka: Pakka):
    hands = len(pelaajat)
    #pelaajien kortit
    for i in range(2):
        for i in range(hands):
            kortti = pakka.jaa()
            player = pelaajat[i]
            player.hand.append(kortti)


    # burnit sekä kortit
    flop = []
    turn = ""
    river = ""
    #poltto
    pakka.jaa()
    #flop
    for i in range(3):
        kortti = pakka.jaa()
        flop.append(kortti)
    # turn
    turn = pakka.jaa()
    # river
    river = pakka.jaa()

    for pelaaja in pelaajat:
        print(pelaaja.name)
        for item in pelaaja.hand:
            print(item)
    
    print("flop")
    for item in flop:
        print(item)

    print("turn")
    print(turn)

    print("river")
    print(river)

def main_kasi():
    pakka = Pakka()
    pakka.kasaa()
    pakka.sekoita()
    pelaajat = make_a_table(5)
    hand(pelaajat, pakka)

# Käsien tunnistus
# tunnistaa käden viidellä kortilla

# palautettavaksi asetettava käden arvo tai tehtävä vertailualgo, jotta myöhemmin (paska O) voi kokeilla kombinaatiot 5 community 0 hole, 4 c 1 h, 3 c 2 h
def onko_vari(kortit: list):
    eka_maa = kortit[0].maa
    for kortti in kortit[1:]:
        if kortti.maa != eka_maa:
            return False
    return True, eka_maa

def onko_suora(kortit: list):
    numerolista = []
    for kortti in kortit:
        numerolista.append(kortti.arvo)
    numerolista.sort()

    if numerolista == [1, 10, 11, 12, 13]:
        return True, 14
    for i in range(1, 5):
        if numerolista[i] != numerolista[i - 1] + 1:
            return False
    return True, numerolista[-1]

def neloset(kortit: list):
    lista = []
    for kortti in kortit:
        lista.append(kortti.arvo)
    for arvo in lista:
        if lista.count(arvo) == 4:
            return (True, arvo)

def fullhouse(kortit: list):
    # palauttaa joko (True, trips arvo, pari arvo) tai False
    lista = []
    for kortti in kortit:
        lista.append(kortti.arvo)
    if len(set(lista)) != 2:
        return False
    else:
        trips = 0
        pari = 0
        for kortti in kortit:
            if lista.count(kortti.arvo) == 3:
                trips = kortti.arvo
            elif lista.count(kortti.arvo) == 2:
                pari = kortti.arvo
        
        return (True, trips, pari)

def trips(kortit: list):
    # palauttaa True ja kortti jota kolme
    lista = []
    for kortti in kortit:
        lista.append(kortti.arvo)
    for kortti in lista:
        if lista.count(kortti) == 3:
            return (True, kortti)
    return False

def two_pair(kortit):
    cards = []
    for kortti in kortit:
        cards.append(kortti.arvo)
    if len(set(cards)) == 3:
        parit = []
        for card in cards:
            if cards.count(card) == 2:
                if card == 1:
                    parit.append(14)
                    cards.remove(1)
                else:
                    parit.append(card)
                    cards.remove(card)
        parit.sort(reverse=True)
        return True, parit
    return False

def pair(kortit: list):
    lista = []
    for kortti in kortit:
        lista.append(kortti.arvo)
    for card in lista:
        if lista.count(card) == 2:
            return (True, card)
    return False

def hicard(kortit: list):
    # muuttaa ässän 14, muuten normaali ja palauttaa numerot järjestyksessä
    lista = []
    for kortti in kortit:
        if kortti.arvo == 1:
            lista.append(14)
        else:
            lista.append(kortti.arvo)
    return sorted(lista, reverse=True)


# määrittele_käsi toimii
def maarittele_kasi(kortit: list):
    if onko_suora(kortit) and onko_vari(kortit):
        return f"{onko_vari(kortit)[1]}värisuora, suurin {onko_suora(kortit)[1]}"

    elif neloset(kortit):
        return f"{neloset(kortit)[1]}-neloset"

    elif fullhouse(kortit):
        return f"full house, {fullhouse(kortit)[1]} täynnä {fullhouse(kortit)[2]}"

    elif onko_vari(kortit):
        return f"{onko_vari(kortit)[1]}väri"

    elif onko_suora(kortit):
        return f"suora, {onko_suora(kortit)[1]}"

    elif trips(kortit):
        return f"{trips(kortit)[1]}-kolmoset"

    elif two_pair(kortit):
        return f"kaksi paria, {two_pair(kortit)[1][0]} ja {two_pair(kortit)[1][1]}"

    elif pair(kortit):
        return f"{pair(kortit)[1]}-pari"

    else:
        return f"High card {hicard(kortit)[0]}"

def kaden_arvo(kortit: list):
    if onko_suora(kortit) and onko_vari(kortit):
        return 9, onko_suora(kortit)[1]

    elif neloset(kortit):
        return 8, neloset(kortit)[1]

    elif fullhouse(kortit):
        return 7, fullhouse(kortit)[1], fullhouse(kortit)[2]

    elif onko_vari(kortit):
        return 6

    elif onko_suora(kortit):
        return 5, onko_suora(kortit)[1]

    elif trips(kortit):
        return 4, trips(kortit)[1]

    elif two_pair(kortit):
        return 3, two_pair(kortit)[1][0], two_pair(kortit)[1][1]

    elif pair(kortit):
        return 2, pair(kortit)[1]

    else:
        return 1, hicard(kortit)


pakka = Pakka()
pakka.kasaa()
pakka.sekoita()

korttipino = []

print(kaden_arvo(korttipino))

print(maarittele_kasi(korttipino))
