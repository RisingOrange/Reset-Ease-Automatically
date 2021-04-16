import datetime
from ast import literal_eval

from anki.lang import _
from aqt import mw
from aqt.utils import getFile, getSaveFile, tooltip


def add_deck_options(menu, deck_id):
    export_action = menu.addAction("Export Ease Factors")
    export_action.triggered.connect(lambda _,
                                    did=deck_id: export_ease_factors(did))
    import_action = menu.addAction("Import Ease Factors")
    import_action.triggered.connect(lambda _,
                                    did=deck_id: import_ease_factors(did))


def export_ease_factors(deck_id):
    '''For some deck `deck_id`, returns a dictionary linking card id keys to
    ease factors.
    '''
    deck_name = mw.col.decks.nameOrNone(deck_id)
    if deck_name is None:
        return
    
    # open file picker to store factors
    dt_now_str = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    suggested_filename = f"ease_factors_{deck_id}_{dt_now_str}"
    export_file = getSaveFile(mw, _("Export"), "export", 
                              key = "",
                              ext = "",
                              fname=suggested_filename)
    if not export_file:
        return

    factors = {}
    card_ids = mw.col.findCards(f'deck:"{deck_name}"')
    for card_id in card_ids:
        card = mw.col.getCard(card_id)
        factors[card_id] = card.factor
    with open(export_file, 'w') as export_file_object: 
        export_file_object.write(str(factors))

    tooltip('Ease Factors were exported')
    


def import_ease_factors(deck_id):
    '''For deck `deck_id` and `factors`--a dictionary linking card id keys to
    ease factors--set the ease factors of the cards in the deck to the ease
    factors provided in `factors`.
    '''
    deck_name = mw.col.decks.nameOrNone(deck_id)
    
    # open file picker to load factors
    import_file = getFile(mw, _("Import"), None, 
                            key = "import")
    
    if not import_file:
        return

    with open(import_file, 'r') as import_file_object:
        factors = literal_eval(import_file_object.read())
        
    card_ids = mw.col.findCards(f'deck:"{deck_name}"')
    for card_id in card_ids:
        card = mw.col.getCard(card_id)
        if card.factor == factors.get(card_id, None):
            continue
        card.factor = factors.get(card_id, card.factor)
        card.flush()

    tooltip('Ease Factors were imported')
