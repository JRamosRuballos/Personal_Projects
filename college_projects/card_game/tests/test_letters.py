import pytest
from src.letters import LettersGame
from src.base import CardType
from letters import Card



def test_create_letters_game_3x4(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (3, 4), 2)
    
    assert game.nrows == 3
    assert game.ncols == 4
    assert game.fit_size == 3
    assert game.num_players == 2
    assert not game.lightning
    assert not game.done
    assert game.scores == {1: 0, 2: 0}


def test_create_letters_game_5x5(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (5, 5), 2)
    
    assert game.nrows == 5
    assert game.ncols == 5
    assert game.fit_size == 3
    assert game.num_players == 2
    assert not game.lightning
    assert not game.done
    assert game.scores == {1: 0, 2: 0}


def test_create_letters_game_9x9(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (9, 9), 2)
    
    assert game.nrows == 9
    assert game.ncols == 9
    assert game.fit_size == 3
    assert game.num_players == 2
    assert not game.lightning
    assert not game.done
    assert game.scores == {1: 0, 2: 0}


def test_tableau_3x4(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (3, 4), 2)
    tableau = game.tableau
    assert len(tableau) == 3
    assert all(len(row) == 4 for row in tableau)

    for r in range(3):
        for c in range(4):
            assert tableau[r][c] in standard_deck


def test_tableau_5x5(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (5, 5), 2)
    tableau = game.tableau
    assert len(tableau) == 5
    assert all(len(row) == 5 for row in tableau)

    for r in range(5):
        for c in range(5):
            assert tableau[r][c] in standard_deck


def test_tableau_9x9(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (9, 9), 2)
    tableau = game.tableau
    assert len(tableau) == 9
    assert all(len(row) == 9 for row in tableau)

    for r in range(9):
        for c in range(9):
            assert tableau[r][c] in standard_deck


def test_card_at_3x4(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (3, 4), 2)
    
    tableau = game.tableau
    assert len(tableau) == 3
    assert all(len(row) == 4 for row in tableau)

    for r in range(3):
        for c in range(4):
            assert game.card_at((r, c)) in standard_deck


def test_call_fit_1(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (3, 4), 2)
    
    positions = [(0, 0), (0, 1), (0, 2)]
    
    game.call_fit(1, positions)

    tableau = game.tableau
    for r, c in positions:
        assert tableau[r][c] in standard_deck
    
    for r, c in positions:
        assert game.card_at((r, c)) in standard_deck

    assert game.scores == {1: 3, 2: 0}
    assert not game.done


def test_call_fit_2(standard_deck: list[CardType]) -> None:
    game = LettersGame(standard_deck, 3, (3, 4), 2)
    
    positions = [(0, 0), (1, 0), (2, 0)]

    game.call_fit(1, positions)

    tableau = game.tableau
    for r, c in positions:
        assert tableau[r][c] in standard_deck

    assert game.scores == {1: 3, 2: 0}
    assert not game.done


# Tests from Milestone #2

def test_moonshot_success(standard_deck_no_fits: list[CardType]) -> None:
    """
    Test that a player is awarded the correct amount of points if they shoot the 
    moon successfully. Also verifis that all cards have been replaced on the 
    tableau.
    """

    game = LettersGame(standard_deck_no_fits, 3, (3, 4), 2)

    game.moonshot_start(1) # assume player 1 called moonshot?
    assert game.moonshot

    game.moonshot_end()
    assert game.scores[1] == 12

    og_cards = set(tuple(card.items()) for card in standard_deck_no_fits)
    
    tableau_cards = set(
        tuple(card.items()) for row in game.tableau for card in row if card
        )

    assert tableau_cards != og_cards

    assert all(card is not None for row in game.tableau for card in row)


def test_moonshot_fail(standard_deck_no_fits: list[CardType]) -> None:
    """
    Test that a player is deducted the correct amount of points if they shoot 
    the moon unsuccessfully because another player calls a valid fit during the 
    moonshot.
    """

    game = LettersGame(standard_deck_no_fits, 3, (3, 4), 2)
    og_cards = [card.copy() for row in game.tableau for card in row if card]

    game.moonshot_start(1)  
    assert game.moonshot
    
    # assume positions (0,0), (0,1), and (0, 2) form a valid fit
    game._tableau.grid[0][0] = Card({"letter": "A", "number": "1", "color": "red", "font": "serif"})
    game._tableau.grid[0][1] = Card({"letter": "B", "number": "2", "color": "green", "font": "sans-serif"})
    game._tableau.grid[0][2] = Card({"letter": "C", "number": "3", "color": "blue", "font": "monospace"})
    game.call_fit(2, [(0, 0), (0, 1), (0, 2)])


    assert game.scores[1] == -12

    tableau_cards = [card for row in game.tableau for card in row if card]

    assert og_cards != tableau_cards
    assert all(card is not None for row in game.tableau for card in row)


def test_lightning_mode_call_fit(standard_deck: list[CardType]) -> None:
    """
    Test that the game ends in lightning mode if a player calls a fit 
    successfully, that player is the winner.
    """

    game = LettersGame(standard_deck, 3, (3,4), 2, lightning=True)

                
    # valid fit tableau
    game.tableau[0][0] = {"letter": "A", "number": "1", "color": "red", "font": "serif"}
    game.tableau[0][1] = {"letter": "A", "number": "2", "color": "green", "font": "sans-serif"}
    game.tableau[0][2] = {"letter": "A", "number": "3", "color": "blue", "font": "monospace"}
    
    # player 1 called valid fit
    game.call_fit(1, [(0, 0), (0, 1), (0, 2)])

    # game ends, player 1 is winner
    assert game.done
    assert game.outcome == {1} 


def test_lightning_mode_moonshot_success(standard_deck: list[CardType]) -> None:
    """
    Test that the game ends in lightning mode if a player successfully shoots 
    the moon, that player is the winner.
    """

    game = LettersGame(standard_deck, 3, (3, 4), 2, lightning = True)

    game.moonshot_start(1)  # assume player 1 starts moonshot
    game.moonshot_end()

    # game ends, player 1 is winner
    assert game.done
    assert game.outcome == {1}


def test_lightning_mode_moonshot_fail(standard_deck: list[CardType]) -> None:
    """
    Test that if a player unsuccessfully shoots the moon in lightning mode,
    they are eliminated from the game.
    """
    
    game = LettersGame(standard_deck, 3, (3, 4), 2, lightning = True) # game with 4 players
    
    # valid fit tableau
    game.tableau[0][0] = {"letter": "A", "number": "1", "color": "red", "font": "serif"}
    game.tableau[0][1] = {"letter": "A", "number": "2", "color": "green", "font": "sans-serif"}
    game.tableau[0][2] = {"letter": "A", "number": "3", "color": "blue", "font": "monospace"}
    
    game.moonshot_start(1)  # assume player 1 starts the moonshot
    game.call_fit(2, [(0, 0), (0, 1), (0, 2)])
    
    assert 1 not in game.active_players # check if player 1 is eliminated


def test_lightning_mode_last_player_wins(standard_deck: list[CardType]) -> None:
    """
    Test that if all players are eliminated except one in lightning mode, that
    player is the winner.
    """
    
    game = LettersGame(standard_deck, 3, (3, 4), 2, lightning= True) # game with 4 players
    
    # player 1, 2, 3 fail moonshot
    game.moonshot_start(1)
    game.call_fit(2, [(0, 0), (0, 1), (0, 2)])

    # player 2 should be the winner
    assert game.done
    assert game.outcome == {2}


def test_validate_enough_cards(standard_deck: list[CardType]) -> None:
    """
    Test that the constructor raises a ValueError if the number of cards
    in the deck is less than nrows * ncols
    """
    with pytest.raises(ValueError):
        LettersGame(standard_deck[:10], 3, (3, 4), 2)


def test_validate_tableau_size(standard_deck: list[CardType]) -> None:
    """
    Test that the constructor raises a ValueError if the number of cards
    in one tableau is less than the fit size.
    """
    with pytest.raises(ValueError):
        LettersGame(standard_deck, 3, (1, 1), 2)


def test_validate_cards_same_features(standard_deck: list[CardType]) -> None:
    """
    Test that the constructor raises a ValueError if the cards in the deck
    do not all have the same feature names
    """
    standard_deck[1] = {"letter": "A", "color": "red", "font": "serif"}
    standard_deck[-1] = {"foo": "1", "bar": "2", "baz": "3"}

    with pytest.raises(ValueError):
        LettersGame(standard_deck, 3, (3, 4), 2)


def test_validate_number_of_feature_values(
    standard_deck: list[CardType],
) -> None:
    """
    Test that the constructor raises a ValueError if the cards
    do not have, for each feature, exactly `fit_size` distinct values.
    (across all card)
    """
    standard_deck[1]["letter"] = "D"
    standard_deck[7]["letter"] = "E"
    standard_deck[10]["color"] = "off white"
    standard_deck[20]["color"] = "cerulean"

    with pytest.raises(ValueError):
        LettersGame(standard_deck, 3, (3, 4), 2)


def test_validate_no_duplicate_cards(standard_deck: list[CardType]) -> None:
    """
    Test that the constructor raises a ValueError if the deck
    contains duplicate cards
    """
    standard_deck[1] = standard_deck[0]
    standard_deck[10] = standard_deck[20]

    with pytest.raises(ValueError):
        LettersGame(standard_deck, 3, (3, 4), 2)


def test_validate_card_at(standard_deck: list[CardType]) -> None:
    """
    Test that card_at raises a ValueError if the position is invalid
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    with pytest.raises(ValueError):
        game.card_at((-1, 0))

    with pytest.raises(ValueError):
        game.card_at((3, 0))

    with pytest.raises(ValueError):
        game.card_at((0, -1))

    with pytest.raises(ValueError):
        game.card_at((0, 4))


def test_call_fit_validate_position_outside_tableau(
    standard_deck: list[CardType],
) -> None:
    """
    Test that call_fit raises a ValueError if any of the positions
    in the list are outside the bounds of the tableau
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    with pytest.raises(ValueError):
        game.call_fit(1, [(-1, 0), (0, 1), (0, 2)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 1), (0, 4), (0, 2)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(7, 7), (-5, -6), (-1, -1)])


def test_call_fit_validate_position_not_empty() -> None:
    """
    Test that call_fit raises a ValueError if any of the positions
    in the list are not empty
    """

    standard_deck_with_fit = [
    # Row 0:
    {"letter": "A", "number": "1", "color": "red",    "font": "serif"},         # index 0  (position (0,0)) - part of fit
    {"letter": "A", "number": "2", "color": "green",  "font": "sans-serif"},    # index 1  (position (0,1)) - part of fit
    {"letter": "B", "number": "3", "color": "blue",   "font": "serif"},         # index 2  (position (0,2))
    {"letter": "C", "number": "1", "color": "green",  "font": "monospace"},     # index 3  (position (0,3))

    # Row 1:
    {"letter": "B", "number": "1", "color": "red",    "font": "sans-serif"},    # index 4  (position (1,0))
    {"letter": "C", "number": "2", "color": "blue",   "font": "sans-serif"},    # index 5  (position (1,1))
    {"letter": "A", "number": "3", "color": "blue",   "font": "monospace"},     # index 6  (position (1,2)) - part of fit
    {"letter": "B", "number": "2", "color": "green",  "font": "monospace"},     # index 7  (position (1,3))

    # Row 2:
    {"letter": "C", "number": "3", "color": "red",    "font": "sans-serif"},    # index 8  (position (2,0))
    {"letter": "B", "number": "3", "color": "green",  "font": "serif"},         # index 9  (position (2,1))
    {"letter": "C", "number": "1", "color": "blue",   "font": "serif"},         # index 10 (position (2,2))
    {"letter": "A", "number": "2", "color": "red",    "font": "monospace"},     # index 11 (position (2,3))
]

    game = LettersGame(standard_deck_with_fit, 3, (3, 4), 2)


    # With the 12-card deck, this will result in these three
    # cards being removed and not replaced
    game.call_fit(1, [(0, 0), (0, 1), (1, 2)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1), (1, 2)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1), (1, 2)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1), (1, 2)])


def test_call_fit_validate_repeated_position(
    standard_deck: list[CardType],
) -> None:
    """
    Test that call_fit raises a ValueError if any of the positions
    in the list are repeated
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1), (0, 1)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1), (0, 0)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 0), (0, 0)])


def test_call_fit_validate_fit_size(standard_deck: list[CardType]) -> None:
    """
    Test that call_fit raises a ValueError if the number of positions
    in the list is not equal to the fit size
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1), (0, 2), (0, 3)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])


def test_call_fit_validate_player(standard_deck: list[CardType]) -> None:
    """
    Test that call_fit raises a ValueError if called
    with an invalid player number.
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    with pytest.raises(ValueError):
        game.call_fit(3, [(0, 0), (0, 1), (0, 2)])

    with pytest.raises(ValueError):
        game.call_fit(-1, [(0, 0), (0, 1), (0, 2)])


def test_moonshot_validate_already_in_moonshot(
    standard_deck: list[CardType],
) -> None:
    """
    Test that moonshot_start raises a ValueError if called
    when the game is already in moonshot mode.
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    game.call_fit(1, [(0, 0), (0, 1), (0, 2)])
    game.call_fit(2, [(1, 1), (1, 2), (1, 3)])

    game.moonshot_start(2)

    with pytest.raises(ValueError):
        game.moonshot_start(1)


def test_moonshot_validate_no_empty_positions() -> None:
    """
    Test that moonshot_start raises a ValueError if called
    when there are empty positions in the tableau.
    """

    standard_deck_with_fit = [
    # Row 0:
    {"letter": "A", "number": "1", "color": "red",    "font": "serif"},         # index 0  (position (0,0)) - part of fit
    {"letter": "A", "number": "2", "color": "green",  "font": "sans-serif"},    # index 1  (position (0,1)) - part of fit
    {"letter": "B", "number": "3", "color": "blue",   "font": "serif"},         # index 2  (position (0,2))
    {"letter": "C", "number": "1", "color": "green",  "font": "monospace"},     # index 3  (position (0,3))

    # Row 1:
    {"letter": "B", "number": "1", "color": "red",    "font": "sans-serif"},    # index 4  (position (1,0))
    {"letter": "C", "number": "2", "color": "blue",   "font": "sans-serif"},    # index 5  (position (1,1))
    {"letter": "A", "number": "3", "color": "blue",   "font": "monospace"},     # index 6  (position (1,2)) - part of fit
    {"letter": "B", "number": "2", "color": "green",  "font": "monospace"},     # index 7  (position (1,3))

    # Row 2:
    {"letter": "C", "number": "3", "color": "red",    "font": "sans-serif"},    # index 8  (position (2,0))
    {"letter": "B", "number": "3", "color": "green",  "font": "serif"},         # index 9  (position (2,1))
    {"letter": "C", "number": "1", "color": "blue",   "font": "serif"},         # index 10 (position (2,2))
    {"letter": "A", "number": "2", "color": "red",    "font": "monospace"},     # index 11 (position (2,3))
]
    game = LettersGame(standard_deck_with_fit, 3, (3, 4), 2)

    # With the 12-card deck, this will result in these three
    # cards being removed and not replaced
    game.call_fit(1, [(0, 0), (0, 1), (1, 2)])

    with pytest.raises(ValueError):
        game.moonshot_start(2)


def test_moonshot_validate_player(standard_deck: list[CardType]) -> None:
    """
    Test that moonshot_start raises a ValueError if called
    with an invalid player number.
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    with pytest.raises(ValueError):
        game.moonshot_start(3)

    with pytest.raises(ValueError):
        game.moonshot_start(-1)


def test_moonshot_end_validate_in_moonshot_mode(
    standard_deck: list[CardType],
) -> None:
    """
    Test that moonshot_end raises a ValueError if called
    when the game is not in moonshot mode.
    """
    game = LettersGame(standard_deck, 3, (3, 4), 2)

    with pytest.raises(ValueError):
        game.moonshot_end()

def test_call_fit_lightning_validate_player(standard_deck: list[CardType]) -> None:
    """
    Check that call_fit raises a ValueError if called with a player that has been eliminated in lightning mode.
    """

    game = LettersGame(standard_deck, 3, (3, 4), 3, lightning=True)
    
    game.tableau[0][0] = {"letter": "A", "number": "1", "color": "red", "font": "serif"}
    game.tableau[0][1] = {"letter": "A", "number": "2", "color": "green", "font": "sans-serif"}
    game.tableau[0][2] = {"letter": "A", "number": "3", "color": "blue", "font": "monospace"}

    game.moonshot_start(1)
    game.call_fit(2, [(0, 0), (0, 1), (0, 2)])

    with pytest.raises(ValueError):
        game.call_fit(1, [(2, 0), (2, 1), (2, 2)])


def test_moonshot_lightning_validate_player(standard_deck: list[CardType]) -> None:
    """
    Check that moonshot_start raises a ValueError if called with a player that has been eliminated in lightning mode.
    """
    game = LettersGame(standard_deck, 3, (3, 4), 3, lightning=True)

    game.moonshot_start(1)
    game.call_fit(2, [(0, 0), (0, 1), (0, 2)])


    with pytest.raises(ValueError):
        game.moonshot_start(1)

def test_call_fit_1_x(extended_deck: list[CardType]) -> None:
    game = LettersGame(extended_deck, 4, (7, 9), 2)
    
    positions = [(0, 0), (0, 1), (0, 2), (0, 3)]
    
    game.call_fit(1, positions)

    tableau = game.tableau
    for r, c in positions:
        assert tableau[r][c] in extended_deck
    
    for r, c in positions:
        assert game.card_at((r, c)) in extended_deck

    assert game.scores == {1: 4, 2: 0}
    assert not game.done


def test_call_fit_2_x(extended_deck: list[CardType]) -> None:
    game = LettersGame(extended_deck, 4, (7, 9), 2)
    
    positions = [(0, 0), (1, 0), (2, 0), (3, 0)]

    game.call_fit(1, positions)

    tableau = game.tableau
    for r, c in positions:
        assert tableau[r][c] in extended_deck

    assert game.scores == {1: -4, 2: 0}
    assert not game.done


def test_moonshot_success_x(extended_deck: list[CardType]) -> None:
    """
    Test that a player is awarded the correct amount of points if they shoot the 
    moon successfully. Also verifies that all cards have been replaced on the 
    tableau.
    """

    game = LettersGame(extended_deck, 4, (7, 9), 2)

    game.moonshot_start(1)  # Assume player 1 called moonshot?
    assert game.moonshot

    game.moonshot_end()
    assert game.scores[1] == 63  # 7 * 9 = 63 points for tableau size

    og_cards = set(tuple(card.items()) for card in extended_deck)
    tableau_cards = set(
        tuple(card.items()) for row in game.tableau for card in row if card
    )

    assert tableau_cards != og_cards

    assert all(card is not None for row in game.tableau for card in row)


def test_moonshot_fail_x(extended_deck: list[CardType]) -> None:
    """
    Test that a player is deducted the correct amount of points if they shoot 
    the moon unsuccessfully because another player calls a valid fit during the 
    moonshot.
    """

    game = LettersGame(extended_deck, 4, (7, 9), 2)
    og_cards = [card.copy() for row in game.tableau for card in row if card]

    game.moonshot_start(1)  
    assert game.moonshot
    
    game.tableau[0][0] = {"letter": "A", "number": "1", "color": "red", "font": "serif"}
    game.tableau[0][1] = {"letter": "B", "number": "2", "color": "green", "font": "sans-serif"}
    game.tableau[0][2] = {"letter": "C", "number": "3", "color": "blue", "font": "monospace"}
    game.tableau[0][3] = {"letter": "D", "number": "4", "color": "yellow", "font": "serif"}
    game.call_fit(2, [(0, 0), (0, 1), (0, 2), (0, 3)])

    assert game.scores[1] == -63

    tableau_cards = [card for row in game.tableau for card in row if card]

    assert og_cards != tableau_cards
    assert all(card is not None for row in game.tableau for card in row)
