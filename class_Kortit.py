# cards
from audioop import reverse
from random import shuffle as shuffle


class Card:
    def __init__(self, value: int, suit: str):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.suit} {self.value}"


class Deck:
    def __init__(self):
        self.deck = []

    def make_deck(self):
        suits = ["Heart", "Diamond", "Spade", "Club"]
        for suit in suits:
            for n in range(1, 14):
                card = Card(n, suit)
                self.deck.append(card)

    def shuffle(self):
        shuffle(self.deck)

    # deals the top card
    def deal(self):
        card = self.deck[-1]
        self.deck.remove(card)
        return card


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = []

#
# Deck works
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
        player = Player(name)
        players.append(player)
    return players

# Hand
# this function will probably become obsolete


def hand(players: list, deck: Deck):
    hands = len(players)
    # deals cards for the players
    for i in range(2):
        for i in range(hands):
            card = deck.deal()
            player = players[i]
            player.hand.append(card)

    # burns and cards
    flop = []
    turn = ""
    river = ""
    # burn
    deck.deal()
    # flop
    for i in range(3):
        card = deck.deal()
        flop.append(card)
    # turn
    turn = deck.deal()
    # river
    river = deck.deal()

    for player in players:
        print("")
        print(player.name)
        for item in player.hand:
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
    deck = Deck()
    deck.make_deck()
    deck.shuffle()
    players = make_a_table()
    hand(players, deck)

# hand recognition


def is_suited(cards: list):
    first_card_suit = cards[0].suit
    for card in cards[1:]:
        if card.suit != first_card_suit:
            return False
    return True, first_card_suit


def is_straight(cards: list):
    num_list = []
    for card in cards:
        num_list.append(card.value)
    num_list.sort()

    if num_list == [1, 10, 11, 12, 13]:
        return True, 14
    for i in range(1, 5):
        if num_list[i] != num_list[i - 1] + 1:
            return False
    return True, num_list[-1]


def four_of_a_kind(cards: list):
    cardlist = []
    for card in cards:
        cardlist.append(card.value)
    for value in cardlist:
        if cardlist.count(value) == 4:
            return (True, value)


def fullhouse(cards: list):
    # returns either (True, value of trips, value of pair) or False
    cardlist = []
    for card in cards:
        cardlist.append(card.value)
    if len(set(cardlist)) != 2:
        return False
    else:
        trips = 0
        pair = 0
        for card in cards:
            if cardlist.count(card.value) == 3:
                trips = card.value
            elif cardlist.count(card.value) == 2:
                pair = card.value

        return (True, trips, pair)


def trips(cards: list):
    # returns (True, value of trips)
    cardlist = []
    for card in cards:
        cardlist.append(card.value)
    for card in cardlist:
        if cardlist.count(card) == 3:
            return (True, card)
    return False


def two_pair(cards):
    cards = []
    for card in cards:
        cards.append(card.arvo)
    if len(set(cards)) == 3:
        pairs = []
        for card in cards:
            if cards.count(card) == 2:
                if card == 1:
                    pairs.append(14)
                    cards.remove(1)
                else:
                    pairs.append(card)
                    cards.remove(card)
        pairs.sort(reverse=True)
        return True, pairs
    return False


def pair(cards: list):
    cardlist = []
    for card in cards:
        cardlist.append(card.value)
    for card in cardlist:
        if cardlist.count(card) == 2:
            return (True, card.value)
    return False


def hicard(cards: list):
    # Ace = 14, returns sorted list, reverse is true
    cardlist = []
    for card in cards:
        if card.arvo == 1:
            cardlist.append(14)
        else:
            cardlist.append(card.arvo)
    return sorted(cardlist, reverse=True)


def name_hand(cards: list):
    if is_straight(cards) and is_suited(cards):
        return f"{is_suited(cards)[1]}straight flush, from {is_straight(cards)[1] - 4} to {is_straight(cards)[1]}"

    elif four_of_a_kind(cards):
        return f"Four {four_of_a_kind(cards)[1]}s"

    elif fullhouse(cards):
        return f"full house, {fullhouse(cards)[1]}s full of {fullhouse(cards)[2]}s"

    elif is_suited(cards):
        return f"{is_suited(cards)[1]}-suit"

    elif is_straight(cards):
        return f"straight, {is_straight(cards)[1]-4} to {is_straight(cards)[1]}"

    elif trips(cards):
        return f"Three of a kind, {trips(cards)[1]}s"

    elif two_pair(cards):
        return f"Two pair, {two_pair(cards)[1][0]}s and {two_pair(cards)[1][1]}s"

    elif pair(cards):
        return f"Pair, {pair(cards)[1]}s"

    else:
        return f"High card {hicard(cards)[0]}"


# return the valuation of the hand, the cards needed for evaluation between hands of same valuation and
# as a last item, (use -1 as index) all the cards for hiCard evals


def evaluate_hand(cards: list):
    if is_straight(cards) and is_suited(cards):
        return 9, is_straight(cards)[1], cards

    elif four_of_a_kind(cards):
        return 8, four_of_a_kind(cards)[1], cards

    elif fullhouse(cards):
        return 7, fullhouse(cards)[1], fullhouse(cards)[2], cards

    elif is_suited(cards):
        return 6, cards

    elif is_straight(cards):
        return 5, is_straight(cards)[1], cards

    elif trips(cards):
        return 4, trips(cards)[1], cards

    elif two_pair(cards):
        return 3, two_pair(cards)[1][0], two_pair(cards)[1][1], cards

    elif pair(cards):
        return 2, pair(cards)[1], cards

    else:
        return 1, hicard(cards), cards


def make_a_table():
    # loop for making players
    players = []
    MorePlayers = True
    while MorePlayers:
        name = input("name:")
        if name == "":
            MorePlayers = False
            break
        player = Player(name)
        players.append(player)
    return players

# Hand player


def hand2(players: list, pakka: Deck):
    hands = len(players)
    # players cards
    for i in range(2):
        for i in range(hands):
            kortti = pakka.deal()
            player = players[i]
            player.hand.append(kortti)

    community_cards = []
    for i in range(5):
        community_cards.append(pakka.deal())

    return community_cards, players


def main_hand():
    pakka = Deck()
    pakka.kasaa()
    pakka.sekoita()
    players = make_a_table()
    return hand2(players, pakka)


peli = main_hand()


# player by looping thru main_hand return value players,
def hand_variations(player: Player, community_cards: list):
    # community card by from main_hand return value community_cards
    holecards = player.hand
    communitycards = community_cards

    variations = []
    variations.append(communitycards)

    # 1 holecard, 4 community cards

    #### THIS THING #####
    # makes all subgroups of four cards from five community cards, same logic will follow for subgroups of 3

    ccl1 = communitycards[:]  # community card list 1
    cc1 = ccl1.pop(-1)  # community card 1
    vccl1 = ccl1[:]  # variable ccl1

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
