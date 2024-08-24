import sys
import wx
from wx_ribbon import themes, icons
from wx_ribbon.themes.base import RibbonThemeMixin


class FrameRibbon(wx.Panel, RibbonThemeMixin):
    """
    Similar to a wx.Toolbar but with labelled sections and the option to add any wx.Window as a ctrl.

    Parameters
    ----------
    parent : wx.Frame or wx.Window
        Frame or Window to which this ribbon belongs
    """
    def __init__(
            self, 
            parent,
            theme=themes.RB_THEME_LIGHT
        ):
        # initialize panel
        wx.Panel.__init__(self, parent)
        # setup sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        # dicts in which to store sections and buttons
        self.sections = {}
        self.buttons = {}
        # set theme
        self.SetTheme(theme)

    def AddSection(self, name, label=None, icon=None):
        """
        Add a section to the ribbon.

        Parameters
        ----------
        name : str
            Name by which to internally refer to this section
        label : str
            Label to display on the section
        icon : str or None
            File stem of the icon for the section's label

        Returns
        -------
        FrameRibbonSection
            The created section handle
        """
        # create section
        self.sections[name] = sct = FrameRibbonSection(
            self, label=label, icon=icon
        )
        # add section to sizer
        self.sizer.Add(sct, border=0, flag=wx.EXPAND | wx.ALL)

        return sct

    def AddSeparator(self):
        """
        Add a vertical line.
        """
        if sys.platform == "win32":
            # make separator
            sep = wx.StaticLine(self, style=wx.LI_VERTICAL)
            # add separator
            self.sizer.Add(sep, border=6, flag=wx.EXPAND | wx.ALL)
        else:
            # on non-Windows, just use a big space
            self.sizer.AddSpacer(36)

    def AddSpacer(self, size=6, section=None):
        """
        Add a non-streching space.
        """
        # choose sizer to add to
        if section is None:
            sizer = self.sizer
        else:
            sizer = self.sections[section].sizer
        # add space
        sizer.AddSpacer(size=size)

    def AddStretchSpacer(self, prop=1, section=None):
        """
        Add a stretching space.
        """
        # choose sizer to add to
        if section is None:
            sizer = self.sizer
        else:
            sizer = self.sections[section].sizer
        # add space
        sizer.AddStretchSpacer(prop=prop)


class FrameRibbonSection(wx.Panel, RibbonThemeMixin):
    """
    Section within a FrameRibbon, containing controls marked by a label.

    Parameters
    ----------
    parent : FrameRibbon
        Ribbon containing this section
    label : str
        Label to display on this section
    icon : str or None
        File stem of the icon for the section's label
    """
    def __init__(self, parent, label=None, icon=None):
        wx.Panel.__init__(self, parent)
        self.ribbon = parent
        # setup sizers
        self.border = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.border)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.border.Add(self.sizer, proportion=1, border=0, flag=(
            wx.EXPAND | wx.ALL | wx.RESERVE_SPACE_EVEN_IF_HIDDEN
        ))
        # add label sizer
        self.labelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.border.Add(
            self.labelSizer, border=6, flag=wx.ALIGN_CENTRE | wx.TOP
        )
        # add label icon
        self.iconCtrl = wx.StaticBitmap(
            self, bitmap=wx.Bitmap()
        )
        if icon is None:
            self.iconCtrl.Hide()
        self.labelSizer.Add(
            self.iconCtrl, border=6, flag=wx.EXPAND | wx.RIGHT
        )
        self.SetIcon(icon)
        # add label text
        if label is None:
            label = ""
        self.label = wx.StaticText(self, label=label, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.labelSizer.Add(
            self.label, flag=wx.EXPAND
        )
        # inherit theme
        self.InheritTheme()

        # add space
        self.border.AddSpacer(6)

        # dict in which to store buttons
        self.buttons = {}
    
    def SetIcon(self, icon):
        """
        Set the icon for this section (will update with theme).

        Parameters
        ----------
        icon : wx_ribbon.icons.RibbonIcon
            RibbonIcon object containing both light and dark versions of this icon.
        """
        self.icon = icon
    
    def ApplyTheme(self):
        RibbonThemeMixin.ApplyTheme(self)
        # also update icon
        if self.icon is not None:
            self.iconCtrl.SetBitmap(
                self.icon.GetBitmap(height=16, style=self.theme.icons)
            )

        self.Update()
        self.Refresh()
