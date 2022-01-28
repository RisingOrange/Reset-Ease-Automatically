from anki.decks import DeckManager
from aqt import mw


def add_compat_alias(namespace, new_name, old_name):
    if new_name not in list(namespace.__dict__.keys()):
        setattr(namespace, new_name, getattr(namespace, old_name))
        return True

    return False


def setup_compat_aliases():
    add_compat_alias(mw.col, "get_card", "getCard")
    add_compat_alias(mw.col, "find_cards", "findCards")

    if "all_names" not in DeckManager.__dict__.keys():
        if "allNames" in DeckManager.__dict__.keys():
            DeckManager.all_names = DeckManager.allNames
        else:
            DeckManager.all_names = lambda _: [
                name for name, _ in DeckManager.all_names_and_ids()
            ]

    if "all_ids" not in DeckManager.__dict__.keys():
        if "allIds" in DeckManager.__dict__.keys():
            DeckManager.all_ids = DeckManager.allIds
        else:
            DeckManager.all_ids = lambda _: [
                id for _, id in DeckManager.all_names_and_ids()
            ]
