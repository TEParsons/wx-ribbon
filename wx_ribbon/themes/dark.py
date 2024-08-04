import wx
from .base import BaseRibbonTheme, RB_ICONSTYLE_DARK


class DarkRibbonTheme(BaseRibbonTheme):
    name = "DARK"
    # use dark-mode icons for this theme
    icons = RB_ICONSTYLE_DARK
    # darker background shades
    overlay = "#222222"
    crust = "#141414"
    mantle = "#080808"
    base = "#000000"
    # text in white
    text = "#ffffff"