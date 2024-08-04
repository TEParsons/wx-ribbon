import logging
import importlib.metadata


__all__ = [
    "LoadPluginThemes",
    "RB_THEME_LIGHT",
    "RB_THEME_DARK",
]


class ThemeConstantHandler:
    """
    Class used by BaseRibbonTheme to handle adding constants for each new theme. Should not need to 
    be used outside of `base.py` 
    """
    prefix = "RB_THEME_"

    @classmethod
    def RegisterThemeConstant(cls, theme):
        """
        Create a constant for a given theme.

        Parameters
        ----------
        theme : wx_ribbon.themes.base.BaseRibbonTheme
            Theme to register as a constant
        """
        # skip unnamed themes
        if theme.name is None:
            # log warning if class isn't the base class
            if not theme.__name__.startswith("Base"):
                logging.warn(
                    f"Ribbon theme '{theme.__name__}' does not specify a name so will not be "
                    f"available as a constant (`themes.RB_THEME_...`)"
                )
            # skip
            return
        # transform name
        name = theme.name
        name = name.upper()
        name = name.replace(" ", "_")
        # prepend prefix
        name = cls.prefix + name
        # create global constant
        globals()[name] = theme
        # add to __all__
        __all__.append(name)


def LoadPluginThemes():
    """
    Load any themes specified in plugins.

    To add a plugin theme, specify an entry point to `wx_ribbon.themes` in your module.
    """
    # iterate through entry points targeting this module
    for ep in importlib.metadata.entry_points(group="wx_ribbon.themes"):
        # load each (registering the theme)
        try:
            ep.load()
        except Exception as err:
            logging.error(
                f"Failed to load theme {ep.name} from {ep.group}. Reason: {err}"
            )


# load the built-in themes
from .light import LightRibbonTheme
from .dark import DarkRibbonTheme