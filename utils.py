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
        if int(deck_id) in [d.id for d in mw.col.decks.all_names_and_ids()]
    }
    set_value('deck_to_ease', cleaned)

def convert_deck_names_to_ids_in_deck_to_ease():
    converted = {
        (
            mw.col.decks.id_for_name(deck_name_or_id)
            if deck_name_or_id in [d.name for d in mw.col.decks.all_names_and_ids()]
            else deck_name_or_id
        ) : ease
        for deck_name_or_id, ease in get_value('deck_to_ease').items()
    }
    set_value('deck_to_ease', converted)