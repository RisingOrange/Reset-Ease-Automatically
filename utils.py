from aqt import mw

from .config import get_value, set_value


def clean_up_deck_to_ease():

    if not get_value('deck_to_ease'):
        return

    #for backwards-compatibility (previously names were stored instead of ids)
    convert_deck_names_to_ids_in_deck_to_ease()

    cleaned = {
        deck_id : ease
        for deck_id, ease in get_value('deck_to_ease').items()
        if str(deck_id) in mw.col.decks.allIds()
    }
    set_value('deck_to_ease', cleaned)

def convert_deck_names_to_ids_in_deck_to_ease():
    converted = {
        (
            mw.col.decks.id(deck_name_or_id, create=False)
            if deck_name_or_id in mw.col.decks.allNames()
            else deck_name_or_id
        ) : ease
        for deck_name_or_id, ease in get_value('deck_to_ease').items()
    }
    set_value('deck_to_ease', converted)