import random

class Color:
    RED = "red"
    BLACK = "black"

class Shape:
    HEART = "heart"
    DIAMOND = "diamond"
    SPADE = "spade"
    CLUB = "club"

class Value:
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10

class Card:
    def __init__(self, shape, value):
        self.shape = shape
        self.value = value
        if self.shape in [Shape.HEART, Shape.DIAMOND]:
            self.color = Color.RED
        else:
            self.color = Color.BLACK
    
    def __repr__(self):
        return f"{self.value} of {self.shape} {self.color}"


def standard_deck() -> list[Card]:
    """
    This is a function to create a standard 52 card deck.

    Args:
        None

    Returns:
        A list of cards
    """
    deck = []
    shapes = [Shape.HEART, Shape.DIAMOND, Shape.SPADE, Shape.CLUB]
    values = [Value.ACE,
              Value.TWO,
              Value.THREE,
              Value.FOUR,
              Value.FIVE,
              Value.SIX,
              Value.SEVEN,
              Value.EIGHT,
              Value.NINE,
              Value.TEN,
              Value.JACK,
              Value.QUEEN,
              Value.KING
            ]
    for shape in shapes:
        for value in values:
            card = Card(shape, value)
            deck.append(card)
    return deck

deck = standard_deck()

def evaluate_points(deck: list[Card]) -> int:
    """
    Calculates the point value of a deck

    Arg:
        deck (list[Card]): the desired player's deck
    Returns:
        points (int): the point value of the deck
    """
    points = 0
    for card in deck:
        if card.value == 1:
            if points <= 10:
                points += 11
            else:
                points += 1
        else:
            points += card.value

def dealer_move(deck, dealer_deck, dealer_points, player_points):
    """
    Logic for the dealer's move. If the Player stood with a deck of value less
    than 21, the dealer will draw until the value of their deck hits 21 or is
    greater than the Player's deck value.

    Args:
        deck, dealer_deck, dealer_points, player_points
    Returns:
        moves (list[str]): a list of moves consisting of either "Stand" or "Hit"
    """
    moves = []
    while (dealer_points < player_points) or (dealer_points != 21):
        moves.append("Hit")
        dealer.append(random.choice(deck))
        dealer_points += dealer[0].value
    if dealer_points > 21:
        print("Dealer has gone over 21! Dealer lost.")
        print("Player wins!")
    else:
        print(f"Dealer has {dealer_points} points\
               and Player has {player_points} points")
        print("Dealer wins.")


dealer = []
dealer_points = 0
player = []
player_points = 0

dealer.append(random.choice(deck))
dealer_points += dealer[0].value
print("One card was dealt to the dealer")
player.append(random.choice(deck))
player_points += player[0].value
print("One card was dealt to the player")
dealer.append(random.choice(deck))
dealer_points += dealer[1].value
print("A second card was dealt to the dealer")

if dealer_points == 21:
    print("Dealer has a Blackjack! Dealer wins.")
else:
    player_move = input("Hit or Stand?:")
    if player_move == "Hit":
        player.append(random.choice(deck))
        player_points += player[-1].value
        if player_points == 21:
            print("Player has a Blackjack! Player wins.")
        else:
            while (dealer_points < 21) and (player_points < 21):
                player_move = input("Hit or Stand?")
                if player_move == 'Hit':
                    player.append(random.choice(deck))
                    player_points += player[-1].valie
                    print("Another card dealt to the player")
                    r
    




print("Current Player Hand:")
for card in player:
    print(card)
player_move = input("Hit or Stand?: ")

if player_move == "Hit":
    player.append(random.chocie(deck))
    player_points += player[-1].value
    print("Another ard was dealt to the player.")
    print(f"Player now has {player_points} points")
