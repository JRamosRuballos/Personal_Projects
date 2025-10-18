"""
TUI for Milestone #3
"""
import random
import click
from colorama import Fore
from letters import LettersGame
from base import CardType, PositionType

def standard_deck() -> list[CardType]:
    """
    Fixture that return a standard deck of Letters cards.
    Note: when laid out in a 3x4 tableau, all cards will
    have the letter "A" in them, so any three cards
    will be a fit (according to the fake rules, not according
    to the actual rules of Letters)
    """
    letters = ["A", "B", "C"]
    numbers = ["1", "2", "3"]
    colors = ["red", "green", "blue"]
    fonts = ["serif", "sans-serif", "monospace"]

    all_cards = [
        {"letter": letter, "number": number, "color": color, "font": font}
        for letter in letters
        for number in numbers
        for color in colors
        for font in fonts
    ]

    return all_cards

def extended_deck() -> list[CardType]:
    """
    Fixture that returns an extended deck of Letters cards.
    The extended deck includes new features:
    - Letter: A, B, C, D
    - Number: 1, 2, 3, 4
    - Color: Red, Green, Blue, Orange
    - Font: 4 different fonts
    - Border Color: Same options as Color
    """
    letters = ["A", "B", "C", "D"]
    numbers = ["1", "2", "3", "4"]
    colors = ["red", "green", "blue", "orange"]
    fonts = ["serif", "sans-serif", "monospace", "cursive"]
    border_colors = ["red", "green", "blue", "orange"]

    all_cards = [
        {"letter": letter, "number": number, "color": color, "font": font,
         "border_color": border_color}
        for letter in letters
        for number in numbers
        for color in colors
        for font in fonts
        for border_color in border_colors
    ]

    return all_cards

def card_face(card: CardType | None) -> str:
    """
    Creates the TUI display of a card.
    
    Args:
        card: CardType
    
    Returns:
        new_letter: The display of the letter card with correct letter, number
                    of letters, font, color, and boroder color (if applies). 
                    If card is none, returns an empty spaced string.
    """
    if card is None:
        return "     "
    letter = card["letter"]
    font = card["font"]
    color = card["color"]
    border_color = card.get("border_color", "green")
    number = int(card["number"])
    mult_letter = letter * number
    if len(mult_letter) == 1:
        new_letter = "  " + mult_letter + " "
    elif len(mult_letter) == 2:
        new_letter = "  " + mult_letter
    elif len(mult_letter) == 3:
        new_letter = " " + mult_letter
    elif len(mult_letter) == 4:
        new_letter = mult_letter
    if font == "serif":
        new_letter = " " + new_letter.upper() + " "
    elif font == "sans-serif":
        new_letter = " " + new_letter.lower() + " "
    elif font == "monospace":
        new_letter = "*" + new_letter + "*"
    elif font == "cursive":
        new_letter = "~" + new_letter + "~"
    if color == "red":
        new_letter = Fore.RED + new_letter
    elif color == "green":
        new_letter = Fore.GREEN + new_letter
    elif color == "blue":
        new_letter = Fore.BLUE + new_letter
    elif color == "orange":
        new_letter = Fore.YELLOW + new_letter
    if border_color == "red":
        new_letter = f"{Fore.RED}[{new_letter}{Fore.RED}]{Fore.RESET}"
    elif border_color == "green":
        new_letter = f"{Fore.GREEN}[{new_letter}{Fore.GREEN}]{Fore.RESET}"
    elif border_color == "blue":
        new_letter = f"{Fore.BLUE}[{new_letter}{Fore.BLUE}]{Fore.RESET}"
    elif border_color == "orange":
        new_letter = f"{Fore.YELLOW}[{new_letter}{Fore.YELLOW}]{Fore.RESET}"
    return new_letter


def tableau_board(game: LettersGame) -> None:
    """
    Creates a TUI visualization of the tableau board.

    Args:
        game: LettersGame
    
    Returns:
        prints the tableau board
    """
    board = game.tableau
    nrows = game.nrows
    ncol = game.ncols
    for r in range(nrows):
        row_str = ""
        for c in range(ncol):
            element = board[r][c]
            card_text = card_face(element)
            card_format = f"{card_text}"
            row_str += card_format
        print(row_str.strip())

def three_locations(locations: str) -> list[PositionType]:
    """
    Given a string of three card locations, returns a list with a tuple for each
    location.

    Args:
        locations [str]: location of three cards in the format
        'row1,col1 row2,col2 row3,col3'

    Returns:
        tuple_list list[PositionType]: a list with PositionType for each card 
        location
    """
    pairs = locations.split()
    tuple_list = []
    for pair in pairs:
        row, col  = pair.split(',')
        new_row = int(row)
        new_col = int(col)
        tuple_list.append((new_row, new_col))
    return tuple_list

def valid_locations(locations: str) -> bool:
    """
    Given a string, checks whether or not this string contains three card
    locations in the format 'row1,col1 row2,col2 row3,col3'
    """
    pairs = locations.split()
    if not(len(pairs) == 3 or len(pairs) == 4):
        return False
    for pair in pairs:
        try:
            row, col = pair.split(',')
            new_row = int(row)
            new_col = int(col)
        except ValueError:
            return False
    return True

def display_scores(scores: dict[int, int]) -> str:
    """
    Given a dictionary of scores , returns a string representation of scores
    for each player.
    """
    final_str = ""
    for player, score in scores.items():
        final_str += f"P{player}: {score} "
    return final_str

def main_game(row: int, col: int, players: int, ext: bool, fit_s: int) -> None:
    """
    The main TUI game implementation.

    Args:
        row [int]: number of rows
        col [int]: number of columns
        players [int]: number of players
        extended [bool]: whether to use the extended deck
    """
    deck = extended_deck() if ext else standard_deck()
    random.shuffle(deck)
    tableau = LettersGame(deck, fit_s, (row, col), players)
    while not tableau.done:
        tableau_board(tableau)
        print(display_scores(tableau.scores))
        if len(tableau.non_empty_positions) < row * col:
            print("Next player, enter 'no fits left' if all players agree that "
            "there are no more fits.")
        current_player = int(input("Player Number:  "))
        while True:
            action = input("Specify an action:  ")
            if action == "moon":
                tableau.moonshot_start(current_player)
                print("The moon has been shot!")
                while True:
                    calr = int(input("Player Number:  "))
                    moon_action = input("Specify an action:  ")
                    if moon_action == "moon":
                        tableau.moonshot_end()
                        break
                    elif valid_locations(moon_action):
                        if tableau.call_fit(calr, three_locations(moon_action)):
                            print("There is a fit!")
                            print("Moonshot failed :(")
                            break
                        else:
                            print("This is not a fit.")
                            print("Still in moonshot mode.")
                            tableau_board(tableau)
                            print(display_scores(tableau.scores))
                    else:
                        print("Invalid action, try again.")
                break
            elif action == "no fits left":
                tableau.end_game()
                break
            elif valid_locations(action):
                if tableau.call_fit(current_player, three_locations(action)):
                    print("There is a fit!")
                    break
                else:
                    print("This is not a fit.")
                    break
            else:
                print("Invalid action, try again.")
    print("Game is done!")
    print(display_scores(tableau.scores))
    max_score = max(tableau.scores.values())
    winners = [player for player, score in tableau.scores.items() if
               score == max_score]
    print(f"Winners: Player(s) {', '.join(map(str, winners))}")

@click.command()
@click.option("-r", '--rows', default = 3, help = "Number of rows.")
@click.option("-c", "--cols", default = 4, help = "Number of columns.")
@click.option("-n", "--players", default = 4, help = "Number of players.")
@click.option("--extended", is_flag = True, default = False, help = "Use the "
"extended deck.")
def play_game(rows, cols, players, extended):
    """Sets up the game based on click inputs (if available).

     Args:
        rows [int]: number of rows
        cols [int]: number of columns
        players [int]: number of players
        extended [bool]: whether the game is in extended mode

    Returns:
        Plays the main TUI game
    """
    fit_size = 3
    if extended:
        fit_size = 4
    main_game(rows, cols, players, extended, fit_size)

if __name__ == "__main__":
    play_game()
