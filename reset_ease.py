from anki.lang import _
from aqt import mw

from .config import get_value


def reset_ease():
    deck_to_user_ease = get_value("deck_to_ease")
    if not deck_to_user_ease:
        return
    for deck_name, user_ease in deck_to_user_ease.items():
        card_ids = mw.col.find_cards(f'deck:"{deck_name}"')
        for card_id in card_ids:
            card = mw.col.getCard(card_id)
            if card.factor == user_ease_to_ease(user_ease):
                continue
            card.factor = user_ease_to_ease(user_ease)
            card.flush()


def user_ease_to_ease(user_ease):
    return user_ease * 10


def deck_id(deck_name):
    return mw.col.decks.id_for_name(deck_name)
