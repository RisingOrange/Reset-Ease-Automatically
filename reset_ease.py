from anki.decks import DeckManager
from aqt import mw

from .config import get_value 

def reset_ease():
    deck_to_user_ease = get_value("deck_to_ease")
    if not deck_to_user_ease:
        return
    for deck_name, user_ease in deck_to_user_ease.items():
        mw.col.db.execute("update cards set factor = ? where did = ?", user_ease_to_ease(user_ease), deck_id(deck_name))
    mw.reset()

def user_ease_to_ease(user_ease):
    return user_ease * 10

def deck_id(deck_name):
    return DeckManager(mw.col).id_for_name(deck_name)