from aqt import mw

from .config import get_value, set_value


def clean_up_deck_to_ease():

    if not get_value('deck_to_ease'):
        return

    cleaned = {
        deck_id : ease
        for deck_id, ease in get_value('deck_to_ease').items()
        if str(deck_id) in mw.col.decks.allIds()
    }
    set_value('deck_to_ease', cleaned)