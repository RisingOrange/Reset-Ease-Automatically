from anki.decks import DeckManager
from aqt import gui_hooks, mw

from .util import set_last_run_date_to_today, today_is_not_last_run_date

# the ease the decks will be set to
user_ease = 250

# the decks of which the ease will be set
deck_names = [
    'russian movie2anki video morphmanned',
    'russian susb2srs video morphmanned',
    'russian 10 000 sentences easiest to hardest 2',
]

def attempt_run():
    if today_is_not_last_run_date():
        reset_ease_of_selected_decks_and_force_sync()
        set_last_run_date_to_today()

def reset_ease_of_selected_decks_and_force_sync():
    for deck_name in deck_names:
        mw.col.db.execute("update cards set factor = ? where did = ?", user_ease_to_ease(user_ease), deck_id(deck_name))
    mw.reset()

    force_upload_on_next_sync()

def user_ease_to_ease(user_ease):
    return user_ease * 10

def force_upload_on_next_sync():
    mw.col.scm += 1

def deck_id(deck_name):
    return DeckManager(mw.col).id_for_name(deck_name)

gui_hooks.main_window_did_init.append(attempt_run)
