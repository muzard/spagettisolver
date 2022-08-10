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

def make_a_table():
    # loop for making players
    players = []
    MorePlayers = True
    while MorePlayers:
        name = input("name:")
        if name == "":
            MorePlayers = False
            break
        player = Pelaaja(name)
        players.append(player)
    return players

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
        print("")
        print(pelaaja.name)
        for item in pelaaja.hand:
            print(item)
    
    print("")
    print("flop")
    for item in flop:
        print(item)

    print("")
    print("turn")
    print(turn)

    print("")
    print("river")
    print(river)

def main_hand():
    pakka = Pakka()
    pakka.kasaa()
    pakka.sekoita()
    pelaajat = make_a_table()
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

# palauttaa käden arvon, mahdollisen vertailukohteen ja viimeisenä iteminä [-1] kortit mahdollisia hiCard vertailuja varten
def kaden_arvo(kortit: list):
    if onko_suora(kortit) and onko_vari(kortit):
        return 9, onko_suora(kortit)[1], kortit

    elif neloset(kortit):
        return 8, neloset(kortit)[1], kortit

    elif fullhouse(kortit):
        return 7, fullhouse(kortit)[1], fullhouse(kortit)[2], kortit

    elif onko_vari(kortit):
        return 6, kortit

    elif onko_suora(kortit):
        return 5, onko_suora(kortit)[1], kortit

    elif trips(kortit):
        return 4, trips(kortit)[1], kortit

    elif two_pair(kortit):
        return 3, two_pair(kortit)[1][0], two_pair(kortit)[1][1], kortit

    elif pair(kortit):
        return 2, pair(kortit)[1], kortit

    else:
        return 1, hicard(kortit), kortit


def make_a_table():
    # loop for making players
    players = []
    MorePlayers = True
    while MorePlayers:
        name = input("name:")
        if name == "":
            MorePlayers = False
            break
        player = Pelaaja(name)
        players.append(player)
    return players

# Käsi

def hand2(pelaajat: list, pakka: Pakka):
    hands = len(pelaajat)
    #pelaajien kortit
    for i in range(2):
        for i in range(hands):
            kortti = pakka.jaa()
            player = pelaajat[i]
            player.hand.append(kortti)

    community_cards = []
    for i in range(5):
        community_cards.append(pakka.jaa())
    
    return community_cards, pelaajat

def main_hand():
    pakka = Pakka()
    pakka.kasaa()
    pakka.sekoita()
    pelaajat = make_a_table()
    return hand2(pelaajat, pakka)

peli = main_hand()
    
def hand_variations(player: Pelaaja, community_cards: list): # player by looping thru main_hand return value pelaajat,
    # community card by from main_hand return value community_cards
    holecards = player.hand
    communitycards = community_cards

    variations = []
    variations.append(communitycards)

    # 1 holecard, 4 community cards

    ccl1 = communitycards[:] # community card list 1
    cc1 = ccl1.pop(-1) # community card 1
    vccl1 = ccl1[:] # variable ccl1

    four_card_list = []

    four_card_list.append(ccl1)

    vccl1[0] = cc1
    four_card_list.append(vccl1)

    vccl1 = ccl1[:]
    vccl1[1] = cc1
    four_card_list.append(vccl1)

    vccl1 = ccl1[:]
    vccl1[2] = cc1
    four_card_list.append(vccl1)

    vccl1 = ccl1[:]
    vccl1[3] = cc1
    four_card_list.append(vccl1)
    vccl1 = ccl1[:]
# lisäilee pariin ekaan kortin kaksi kertaa ^^

hand_variations(peli[1][0], peli[0])