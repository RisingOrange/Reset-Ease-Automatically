from anki.lang import _
from aqt import mw

from .config import get_value
from .utils import clean_up_deck_to_ease


def reset_ease():
    clean_up_deck_to_ease()
    deck_to_user_ease = get_value("deck_to_ease")
    if not deck_to_user_ease:
        return
    for deck_id, user_ease in deck_to_user_ease.items():
        card_ids = mw.col.find_cards(f'deck:{mw.col.decks.name(deck_id)}')
        for card_id in card_ids:
            card = mw.col.getCard(card_id)
            if card.factor == user_ease_to_ease(user_ease):
                continue
            card.factor = user_ease_to_ease(user_ease)
            card.flush()
    mw.reset()


def user_ease_to_ease(user_ease):
    return user_ease * 10


def deck_id(deck_name):
    return mw.col.decks.id_for_name(deck_name)
