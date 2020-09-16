from aqt import mw

from .config import get_value, set_value


def prepare_deck_to_ease_range():

    # for backwards compatibilty
    convert_ease_to_ease_range()

    if not get_value('deck_to_ease_range'):
        return

    # remove entries of decks that do not exist anki
    cleaned = {
        deck_id : ease_range
        for deck_id, ease_range in get_value('deck_to_ease_range').items()
        if str(deck_id) in mw.col.decks.allIds()
    }
    set_value('deck_to_ease_range', cleaned)

def convert_ease_to_ease_range():

    if not get_value('deck_to_ease'):
        return

    converted = {
        deck_id : (ease, ease)
        for deck_id, ease in get_value('deck_to_ease').items()
    }
    set_value('deck_to_ease_range', converted)
    