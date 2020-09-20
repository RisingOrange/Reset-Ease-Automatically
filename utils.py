from aqt import mw

from .config import get_value, set_value


def prepare_deck_to_ease_range():

    deck_to_ease_range = d if (d := get_value('deck_to_ease_range')) else {}

    # for backwards compatibilty
    deck_to_ease = d if (d := get_value('deck_to_ease')) else {}
    deck_to_ease_range.update(**_to_deck_to_ease_range(deck_to_ease))
    set_value('deck_to_ease', None)

    # remove entries of decks that do not exist in anki
    # and ensure the deck ids are of type int
    cleaned = {
        int(deck_id) : ease_range
        for deck_id, ease_range in deck_to_ease_range.items()
        if str(deck_id) in mw.col.decks.allIds()
    }
    set_value('deck_to_ease_range', cleaned)

def _to_deck_to_ease_range(deck_to_ease):
    converted = {
        deck_id : (ease, ease)
        for deck_id, ease in deck_to_ease.items()
    }
    return converted
    