from anki.lang import _
from aqt import mw

from .config import get_value
from .utils import prepare_deck_to_ease_range


def reset_ease():
    prepare_deck_to_ease_range()
    deck_to_user_ease_range = get_value("deck_to_ease_range")
    if not deck_to_user_ease_range:
        return
    for deck_id, user_ease_range in deck_to_user_ease_range.items():
        ease_min, ease_max = [user_ease_to_ease(x) for x in user_ease_range]
        card_ids = mw.col.findCards(f'deck:"{mw.col.decks.name(deck_id)}"')
        for card_id in card_ids:
            card = mw.col.getCard(card_id)
            if card.factor < ease_min:
                card.factor = ease_min
            elif card.factor > ease_max:
                card.factor = ease_max
            card.flush()

def user_ease_to_ease(user_ease):
    return user_ease * 10


def deck_id(deck_name):
    return mw.col.decks.id(deck_name, create=False)
