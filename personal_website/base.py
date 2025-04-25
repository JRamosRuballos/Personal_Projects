"""
The game mechanism for Blackjack
"""
import random


CardType = dict[]

def standard_deck() -> list[CardType]:
    """
    Creates a standard 52 card deck.
    Colors: red or black
    Value: A, 2, 3, 4, 5, 6, 7, 8, 9, J, Q, K
    Shape: club, spade, heart, diamond
    """
    colors = ["red", "black"]
    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "J", "Q", "K"]
    shapes = ["club", "spade", "heart", "diamond"]
    deck = [{"color": color, "value": value, "shape":shape} for color in colors
            for value in value for shape in shapes]
    return deck

def is_blackjack(dealers_cards: list[CardType]) -> bool | None:
    """
    Checks whether the dealer's intial cards yields a blackjack. Prints an error
    message if the dealer does not have two cards.
    """
    if len(dealers_cards) != 2:
        print("Error. Dealer doesn't have two cards.")
        return
    else:
        first_card = dealers_cards[0]
        second_card = dealers_cards[1]
        ten_value = ["J", "Q", "K"]
        if first_card["value"] in ten_value:
            if second_card["value"] == "A":
                return True
            else:
                return False
        elif first_card["value"] == "A":
            if second_card["value"] in ten_value:
                return True
            else:
                return False

def main_game() -> str:
    card_deck = random.shuffle(standard_deck)
    dealer_deck = card_deck.pop(0)
    player_deck = card_deck.pop(0)
    dealer_deck = card_deck.pop(0)
    player_deck = card_deck.pop(0)
    if is_blackjack(dealer_deck):
        return "Blackjack. Dealer won"
    f