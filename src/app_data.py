from enum import Enum


class AppForm(Enum):
    MENU_FORM = 1
    MAIN_FORM = 2


CurrentWin = AppForm.MENU_FORM

IsRunning = False
