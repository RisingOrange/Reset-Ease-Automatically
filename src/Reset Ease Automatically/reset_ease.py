from anki.consts import CARD_TYPE_RELEARNING, CARD_TYPE_REV
from anki.lang import _
from aqt import mw

from .config import get
from .utils import prepare_deck_to_ease_range


def reset_ease():
    prepare_deck_to_ease_range()
    deck_to_user_ease_range = get("deck_to_ease_range")
    if not deck_to_user_ease_range:
        return
    for deck_id, user_ease_range in deck_to_user_ease_range.items():
        ease_min, ease_max = [user_ease_to_ease(x) for x in user_ease_range]
        card_ids = mw.col.find_cards(f'deck:"{mw.col.decks.name(deck_id)}"')
        for card_id in card_ids:
            card = mw.col.get_card(card_id)

            # Only reset ease for review and relearning cards because only those cards use the ease factor.
            # Cards use learning steps when in the learning phase.
            if card.type not in [CARD_TYPE_REV, CARD_TYPE_RELEARNING]:
                continue

            if card.factor < ease_min:
                card.factor = ease_min
                card.flush()
            elif card.factor > ease_max:
                card.factor = ease_max
                card.flush()


def user_ease_to_ease(user_ease):
    return user_ease * 10


def deck_id(deck_name):
    return mw.col.decks.id(deck_name, create=False)
