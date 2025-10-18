import pytest
from src.base import CardType


@pytest.fixture()
def standard_deck() -> list[CardType]:
    """
    Fixture that returns a standard deck of Letters cards.
    Note: when laid out in a 3x4 tableau, all cards will
    have the letter "A" in them, so any three cards
    will be a fit (according to the fake rules, not the actual rules).
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

@pytest.fixture()
def standard_deck_no_fits() -> list[CardType]:
    """
    Standard deck that doesn't have any fits.
    """
    letters = ["A", "B", "C"]
    numbers = ["1", "2", "3"]
    colors = ["red", "green", "blue"]
    fonts = ["serif", "sans-serif", "monospace"]

    all_cards = [
        {"letter": "C", "number": "2", "color": "green",  "font": "serif"},
        {"letter": "B", "number": "1", "color": "green",  "font": "serif"},
        {"letter": "B", "number": "1", "color": "red",    "font": "monospace"},
        {"letter": "A", "number": "2", "color": "blue",   "font": "serif"},
        {"letter": "C", "number": "1", "color": "green",  "font": "sans-serif"},
        {"letter": "A", "number": "1", "color": "blue",   "font": "sans-serif"},
        {"letter": "C", "number": "3", "color": "blue",   "font": "monospace"},
        {"letter": "C", "number": "3", "color": "blue",   "font": "serif"},
        {"letter": "B", "number": "1", "color": "green",  "font": "monospace"},
        {"letter": "A", "number": "3", "color": "blue",   "font": "serif"},
        {"letter": "B", "number": "3", "color": "green",  "font": "sans-serif"},
        {"letter": "C", "number": "1", "color": "green",  "font": "monospace"},
    ]

    extra_12_cards = [
        {"letter": "A", "number": "1", "color": "red",    "font": "serif"},
        {"letter": "A", "number": "1", "color": "red",    "font": "monospace"},
        {"letter": "A", "number": "2", "color": "red",    "font": "monospace"},
        {"letter": "A", "number": "3", "color": "red",    "font": "serif"},
        {"letter": "B", "number": "2", "color": "red",    "font": "serif"},
        {"letter": "B", "number": "3", "color": "blue",   "font": "monospace"},
        {"letter": "B", "number": "2", "color": "blue",   "font": "sans-serif"},
        {"letter": "B", "number": "2", "color": "green",  "font": "serif"},
        {"letter": "C", "number": "2", "color": "blue",   "font": "sans-serif"},
        {"letter": "C", "number": "3", "color": "green",  "font": "serif"},
        {"letter": "C", "number": "2", "color": "red",    "font": "monospace"},
        {"letter": "A", "number": "2", "color": "green",  "font": "sans-serif"},
    ]

    all_cards += extra_12_cards
    return all_cards

@pytest.fixture()
def extended_deck() -> list[CardType]:
    """
    An extended deck with 5 features and 4 values per feature.
    Used for Letters(X) variant tests.
    """
    garments = ["pants", "shirt", "jacket", "sweater"]
    styles = ["formal", "informal", "casual", "sporty"]
    sizes = ["S", "M", "L", "XL"]
    fabrics = ["cotton", "blend", "synthetic", "wool"]
    seasons = ["summer", "fall", "winter", "spring"]

    cards = [
        {
            "garment": garment,
            "style": style,
            "size": size,
            "fabric": fabric,
            "season": season,
        }
        for garment in garments
        for style in styles
        for size in sizes
        for fabric in fabrics
        for season in seasons
    ]

    return cards

@pytest.fixture()
def twelve_cards() -> list[CardType]:
    """
    Fixture that returns a deck with twelve cards that, when laid out in a 3x4 
    grid, will have at least the following cards that are not a fit:

    - (0, 0), (0, 1), and (0, 2)
    - (0, 0), (1, 0), and (2, 0)
    - (2, 0), (2, 1), and (2, 2)
    """
    return [
        {"letter": "A", "number": "1", "color": "red", "font": "serif"},
        {"letter": "B", "number": "2", "color": "green", "font": "sans-serif"},
        {"letter": "B", "number": "2", "color": "green", "font": "monospace"},
        {"letter": "A", "number": "1", "color": "green", "font": "serif"},
        {"letter": "C", "number": "1", "color": "green", "font": "sans-serif"},
        {"letter": "A", "number": "1", "color": "green", "font": "monospace"},
        {"letter": "A", "number": "1", "color": "blue", "font": "serif"},
        {"letter": "A", "number": "1", "color": "blue", "font": "sans-serif"},
        {"letter": "C", "number": "3", "color": "blue", "font": "monospace"},
        {"letter": "A", "number": "2", "color": "green", "font": "serif"},
        {"letter": "B", "number": "2", "color": "red", "font": "sans-serif"},
        {"letter": "C", "number": "3", "color": "red", "font": "monospace"},
    ]