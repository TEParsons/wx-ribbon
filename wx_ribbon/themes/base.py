import wx
from ..icons import RB_ICONSTYLE_LIGHT, RB_ICONSTYLE_DARK


__all__ = [
    "BaseRibbonTheme",
    "RibbonThemeMixin",
    "RB_ICONSTYLE_LIGHT",
    "RB_ICONSTYLE_DARK",
]


class BaseRibbonTheme:
    # name to refer to the theme by (theme will be accessible as `wx_ribbon.themes.RB_THEME_...`)
    name = None
    # should we use light-mode or dark-mode icons for this theme?
    icons = RB_ICONSTYLE_LIGHT
    # four background shades
    overlay = "#dddddd"
    crust = "#e8e8e8"
    mantle = "#f4f4f4"
    base = "#ffffff"
    # text colors (against background & against highlight)
    text = "#000000"
    hltext = "#ffffff"
    # three highlight colors
    hlprimary = "#00a7f0"
    hlsecondary = "#ffbb02"
    hltertiary = "#f35220"
    hlquaternary = "#82bd01"

    def __init_subclass__(cls):
        """
        When creating a subclass of BaseRibbonTheme, add it to the global list of themes.
        """
        from . import ThemeConstantHandler
        # create constant for this class
        ThemeConstantHandler.RegisterThemeConstant(cls)


class RibbonThemeMixin:
    theme = None

    def SetTheme(self, theme):
        """
        Set the theme for this element. If theme has changed from its last value, will call 
        ApplyTheme to apply the changes from the new theme.

        Parameters
        ----------
        theme : wx_ribbon.themes.base.BaseRibbonTheme
            Theme object to use. Can be any of the `RB_THEME_...` constants in wx_ribbon.themes, 
            as these are all subclasses of BaseRibbonTheme. 
        """
        # keep track of what we're changing from and to
        fromTheme = self.theme
        toTheme = theme
        # if theme has not changed, do nothing further
        if fromTheme is toTheme:
            return
        # update theme reference
        self.theme = toTheme
        # apply new theme
        self.ApplyTheme()
        # cascade down to children
        if hasattr(self, "GetChildren"):
            for child in self.GetChildren():
                if isinstance(child, RibbonThemeMixin):
                    child.SetTheme(theme)    
    
    def ApplyTheme(self):
        """
        Use this element's current theme to style itself.
        """
        # set foreground color
        if hasattr(self, "SetForegroundColour"):
            self.SetForegroundColour(self.theme.text)
        
        # frames should be overlay
        if isinstance(self, wx.Frame):
            self.SetBackgroundColour(self.theme.overlay)
        # panels and buttons should be crust
        if isinstance(self, (wx.Panel, wx.Button)):
            self.SetBackgroundColour(self.theme.crust)
        
        # update
        self.Update()
        self.Refresh()
    
    def InheritTheme(self):
        """
        If this element's parent has a theme, inherit it.
        """
        # get parent
        parent = None
        if hasattr(self, "parent"):
            parent = self.parent
        elif hasattr(self, "GetParent"):
            parent = self.GetParent()
        # set theme if available
        if hasattr(parent, "theme"):
            self.SetTheme(parent.theme)

