import wx, wx.svg
from pathlib import Path


__all__ = [
    "RibbonIcon",
    "RB_ICONSTYLE_LIGHT",
    "RB_ICONSTYLE_DARK",
]


# constants for light/dark style
RB_ICONSTYLE_LIGHT = 1
RB_ICONSTYLE_DARK = 0


class RibbonIcon:
    """
    Class for a ribbon icon. To get the wx.Bitmap object for a given style (light or dark), 
    use GetBitmap.

    Parameters
    ----------
    name : str
        Name to refer to this icon by. It will be made available as a constant via 
        `icons.RB_ICON_...`.
    light : str or pathlib.Path
        Path to the image to use for this icon in light mode
    dark : str or pathlib.Path
        Path to the image to use for this icon in dark mode
    """

    def __init__(self, name, light, dark):
        # store name
        self.name = name
        # store path for light image
        self.light = light
        # store path for dark image
        self.dark = dark
        # dict to cache bitmaps in
        self._cache = {
            RB_ICONSTYLE_LIGHT: {},
            RB_ICONSTYLE_DARK: {},
        }
    
    def GetBitmap(self, height=32, style=RB_ICONSTYLE_LIGHT):
        """
        Get a bitmap of this icon.

        Parameters
        ----------
        height : int
            Number of pixels tall to render the icon as (all ribbon icons are square)
        style : int
            Either wx.icons.RB_ICONSTYLE_LIGHT (default) or wx.icons.RB_ICONSTYLE_DARK
        """
        # return light icon if requested
        if style == RB_ICONSTYLE_LIGHT:
            # if not loaded yet, load now
            if isinstance(self.light, (str, Path)):
                self.light = wx.svg.SVGimage.CreateFromFile(str(self.light))
            # convert to bitmap and cache (if not already cached)
            if height not in self._cache[RB_ICONSTYLE_LIGHT]:
                self._cache[RB_ICONSTYLE_LIGHT][height] = self.light.ConvertToScaledBitmap(
                    size=wx.Size(int(height), int(height))
                )
            print(self._cache[RB_ICONSTYLE_LIGHT][height].GetSize())

            return self._cache[RB_ICONSTYLE_LIGHT][height]
        # return dark icon if requested
        if style == RB_ICONSTYLE_DARK:
            # if not loaded yet, load now
            if isinstance(self.dark, (str, Path)):
                self.dark = wx.svg.SVGimage.CreateFromFile(str(self.dark))
            # convert to bitmap and cache (if not already cached)
            if height not in self._cache[RB_ICONSTYLE_DARK]:
                self._cache[RB_ICONSTYLE_DARK][height] = self.dark.ConvertToScaledBitmap(
                    size=wx.Size(height, height)
                )

            return self._cache[RB_ICONSTYLE_DARK][height]
        # error otherwise
        raise ValueError(
            f"Unrecognised icon style `{style}`, must be one of RB_ICONSTYLE_LIGHT or "
            f"RB_ICONSTYLE_DARK."
        )
