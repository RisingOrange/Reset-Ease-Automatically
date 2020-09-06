from anki.decks import DeckManager
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
            card.factor = user_ease_to_ease(user_ease)
            card.flush()


def store_ease(deck_name):
    '''For some deck `deck_name`, returns a dictionary linking card id keys to
    ease factors.
    '''
    ease_backup = {}
    card_ids = mw.col.find_cards(f'deck:"{deck_name}"')
    for card_id in card_ids:
        card = mw.col.getCard(card_id)
        ease_backup[card_id] = card.factor
    return ease_backup


def restore_ease(deck_name, backup):
    '''For deck `deck_name` and `backup`--a dictionary linking card id keys to
    ease factors--set the ease factors of the cards in the deck to the ease
    factors provided in `backup`.
    '''
    card_ids = mw.col.find_cards(f'deck:"{deck_name}"')
    for card_id in card_ids:
        card = mw.col.getCard(card_id)
        card.factor = backup.get(card_id, card.factor)
        card.flush()


def user_ease_to_ease(user_ease):
    return user_ease * 10


def deck_id(deck_name):
    return DeckManager(mw.col).id_for_name(deck_name)
