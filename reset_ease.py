import datetime
from ast import literal_eval

from anki.decks import DeckManager
from anki.lang import _
from aqt import mw
from aqt.gui_hooks import deck_browser_will_show_options_menu
from aqt.utils import getFile, getSaveFile

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


def export_ease_factors(deck_id):
    '''For some deck `deck_id`, returns a dictionary linking card id keys to
    ease factors.
    '''
    deck_name = mw.col.decks.nameOrNone(deck_id)
    if deck_name is None:
        return
    
    # open file picker to store factors
    dt_now_str = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    suggested_filename = "ease_factors_" + str(deck_id) + dt_now_str
    export_file = getSaveFile(mw, _("Export"), "export", 
                              key = "",
                              ext = "",
                              fname=suggested_filename)
    if not export_file:
        return

    factors = {}
    card_ids = mw.col.find_cards(f'deck:"{deck_name}"')
    for card_id in card_ids:
        card = mw.col.getCard(card_id)
        factors[card_id] = card.factor
    with open(export_file, 'w') as export_file_object: 
         export_file_object.write(str(factors))


def import_ease_factors(deck_id, factors=None):
    '''For deck `deck_id` and `factors`--a dictionary linking card id keys to
    ease factors--set the ease factors of the cards in the deck to the ease
    factors provided in `factors`.
    '''
    deck_name = mw.col.decks.nameOrNone(deck_id)
    if deck_name is None:
        print("Deck name not found on import_ease_factors, exiting...")
        return
    
    if factors is None:
        # open file picker to load factors
        import_file = getFile(mw, _("Import"), None, 
                              key = "import")
        with open(import_file, 'r') as import_file_object:
            factors = literal_eval(import_file_object.read())
        
    card_ids = mw.col.find_cards(f'deck:"{deck_name}"')
    for card_id in card_ids:
        card = mw.col.getCard(card_id)
        card.factor = factors.get(card_id, card.factor)
        card.flush()


def user_ease_to_ease(user_ease):
    return user_ease * 10


def deck_id(deck_name):
    return DeckManager(mw.col).id_for_name(deck_name)


def add_deck_options(menu, deck_id):
    export_action = menu.addAction("Export Ease Factors")
    export_action.triggered.connect(lambda _,
                                    did=deck_id: export_ease_factors(did))
    import_action = menu.addAction("Import Ease Factors")
    import_action.triggered.connect(lambda _,
                                    did=deck_id: import_ease_factors(did))


deck_browser_will_show_options_menu.append(add_deck_options)
