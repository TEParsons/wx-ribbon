import wx
from .base import BaseRibbonTheme, RB_ICONSTYLE_DARK


class DarkRibbonTheme(BaseRibbonTheme):
    name = "DARK"
    # use dark-mode icons for this theme
    icons = RB_ICONSTYLE_DARK
    # darker background shades
    overlay = "#101010"
    crust = "#0c0c0c"
    mantle = "#060606"
    base = "#000000"
    # text in white
    text = "#ffffff"