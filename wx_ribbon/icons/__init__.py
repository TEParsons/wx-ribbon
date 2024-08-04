import logging
from pathlib import Path
from .base import RibbonIcon, RB_ICONSTYLE_LIGHT, RB_ICONSTYLE_DARK


__all__ = [
    "LoadPluginIcons",
    "RB_ICONSTYLE_LIGHT",
    "RB_ICONSTYLE_DARK",
]


class IconConstantHandler:
    """
    Class used by BaseRibbonTheme to handle adding constants for each icon. Should not need to 
    be used outside of `base.py` 
    """
    prefix = "RB_ICON_"

    @classmethod
    def RegisterIconConstant(cls, icon):
        """
        Create a constant for a given theme.

        Parameters
        ----------
        theme : wx_ribbon.icons.base.Icon
            Theme to register as a constant
        """
        # skip unnamed icons
        if icon.name is None:
            # log warning
            logging.warn(
                f"Ribbon icon '{icon}' does not specify a name so will not be "
                f"available as a constant (`themes.RB_ICON_...`)"
            )
            # skip
            return
        # transform name
        name = icon.name
        name = name.upper()
        name = name.replace(" ", "_")
        # prepend prefix
        name = cls.prefix + name
        # create global constant
        globals()[name] = icon
        # add to __all__
        __all__.append(name)


# create icon objects for all base icons
for light in (Path(__file__).parent / "light").glob("*.svg"):
    # get dark file
    dark = Path("dark") / light.name
    # if no dark file, use light
    if not dark.is_file():
        dark = light
    # make icon object
    icon = RibbonIcon(
        name=light.stem,
        light=light,
        dark=dark
    )
    # register icon object
    IconConstantHandler.RegisterIconConstant(icon)
