from aiogram.fsm.state import StatesGroup, State

class UploadMediaState(StatesGroup):
    choose_type = State()       # Anime, Kino, Serial, va h.k.
    title = State()             # Sarlavha
    description = State()       # Tavsif
    poster = State()            # Rasm
    video = State()             # Video (ixtiyoriy)
    confirm = State()           # Tasdiqlash
