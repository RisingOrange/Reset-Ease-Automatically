from aqt import mw

from .config import get_value, set_value


def clean_up_deck_to_ease():

    if not get_value('deck_to_ease_range'):
        return

    cleaned = {
        deck_id : ease_range
        for deck_id, ease_range in get_value('deck_to_ease_range').items()
        if str(deck_id) in mw.col.decks.allIds()
    }
    set_value('deck_to_ease_range', cleaned)