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

    def addSection(self, name, label=None, icon=None):
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

    def addButton(self, section, name, label="", icon=None, tooltip="", callback=None,
                  style=wx.BU_NOTEXT):
        """
        Add a button to a given section.

        Parameters
        ----------
        section : str
            Name of section to add button to
        name : str
            Name by which to internally refer to this button
        label : str
            Label to display on this button
        icon : str
            Stem of icon to use for this button
        tooltip : str
            Tooltip to display on hover
        callback : function
            Function to call when this button is clicked
        style : wx.StyleFlag
            Style flags from wx to control button appearance

        Returns
        -------
        FrameRibbonButton
            The created button handle
        """
        # if section doesn't exist, make it
        if section not in self.sections:
            self.addSection(section, label=section)
        # call addButton method from given section
        btn = self.sections[section].addButton(
            name, label=label, icon=icon, tooltip=tooltip, callback=callback, style=style
        )

        return btn

    def addDropdownButton(self, section, name, label, icon=None, callback=None, menu=None):
        """
        Add a dropdown button to a given section.

        Parameters
        ----------
        section : str
            Name of section to add button to
        name : str
            Name by which to internally refer to this button
        label : str
            Label to display on this button
        icon : str
            Stem of icon to use for this button
        callback : function
            Function to call when this button is clicked
        menu : wx.Menu or function
            Menu to show when the dropdown arrow is clicked, or a function to generate this menu

        Returns
        -------
        FrameRibbonDropdownButton
            The created button handle
        """
        # if section doesn't exist, make it
        if section not in self.sections:
            self.addSection(section, label=section)
        # call addButton method from given section
        btn = self.sections[section].addDropdownButton(
            name, label=label, icon=icon, callback=callback, menu=menu
        )

        return btn

    def addSwitchCtrl(
            self, section, name, labels=("", ""), startMode=0, callback=None, style=wx.HORIZONTAL
    ):
        # if section doesn't exist, make it
        if section not in self.sections:
            self.addSection(section, label=section)
        btn = self.sections[section].addSwitchCtrl(
            name, labels, startMode=startMode, callback=callback, style=style
        )

        return btn

    def addPavloviaUserCtrl(self, section="pavlovia", name="pavuser", frame=None):
        # if section doesn't exist, make it
        if section not in self.sections:
            self.addSection(section, label=section)
        # call addButton method from given section
        btn = self.sections[section].addPavloviaUserCtrl(name=name, ribbon=self, frame=frame)

        return btn

    def addPavloviaProjectCtrl(self, section="pavlovia", name="pavproject", frame=None):
        # if section doesn't exist, make it
        if section not in self.sections:
            self.addSection(section, label=section)
        # call addButton method from given section
        btn = self.sections[section].addPavloviaProjectCtrl(name=name, ribbon=self, frame=frame)

        return btn

    def addSeparator(self):
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

    def addSpacer(self, size=6, section=None):
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

    def addStretchSpacer(self, prop=1, section=None):
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
        # inherit theme
        self.InheritTheme()
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
        # self._icon = icons.ButtonIcon(icon, size=16)
        # self.icon = wx.StaticBitmap(
        #     self, bitmap=self._icon.bitmap
        # )
        # if icon is None:
        #     self.icon.Hide()
        # self.labelSizer.Add(
        #     self.icon, border=6, flag=wx.EXPAND | wx.RIGHT
        # )
        # add label text
        if label is None:
            label = ""
        self.label = wx.StaticText(self, label=label, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.labelSizer.Add(
            self.label, flag=wx.EXPAND
        )

        # add space
        self.border.AddSpacer(6)

        # dict in which to store buttons
        self.buttons = {}

    def addButton(self, name, label="", icon=None, tooltip="", callback=None, style=wx.BU_NOTEXT):
        """
        Add a button to this section.

        Parameters
        ----------
        name : str
            Name by which to internally refer to this button
        label : str
            Label to display on this button
        icon : str
            Stem of icon to use for this button
        tooltip : str
            Tooltip to display on hover
        callback : function
            Function to call when this button is clicked
        style : wx.StyleFlag
            Style flags from wx to control button appearance

        Returns
        -------
        FrameRibbonButton
            The created button handle
        """
        # create button
        btn = FrameRibbonButton(
            self, label=label, icon=icon, tooltip=tooltip, callback=callback, style=style
        )
        # store references
        self.buttons[name] = self.ribbon.buttons[name] = btn
        # add button to sizer
        flags = wx.EXPAND
        if sys.platform == "darwin":
            # add top padding on Mac
            flags |= wx.TOP
        self.sizer.Add(btn, border=12, flag=flags)

        return btn

    def addDropdownButton(self, name, label, icon=None, callback=None, menu=None):
        """
        Add a dropdown button to this section.

        Parameters
        ----------
        name : str
            Name by which to internally refer to this button
        label : str
            Label to display on this button
        icon : str
            Stem of icon to use for this button
        callback : function
            Function to call when this button is clicked
        menu : wx.Menu or function
            Menu to show when the dropdown arrow is clicked, or a function to generate this menu

        Returns
        -------
        FrameRibbonDropdownButton
            The created button handle
        """
        # create button
        btn = FrameRibbonDropdownButton(
            self, label=label, icon=icon, callback=callback, menu=menu
        )
        # store references
        self.buttons[name] = self.ribbon.buttons[name] = btn
        # add button to sizer
        self.sizer.Add(btn, border=0, flag=wx.EXPAND | wx.ALL)

        return btn

    def addSwitchCtrl(self, name, labels=("", ""), startMode=0, callback=None, style=wx.HORIZONTAL):
        # create button
        btn = FrameRibbonSwitchCtrl(
            self, labels, startMode=startMode, callback=callback, style=style
        )
        # store references
        self.buttons[name] = self.ribbon.buttons[name] = btn
        # add button to sizer
        self.sizer.Add(btn, border=0, flag=wx.EXPAND | wx.ALL)

        return btn


class FrameRibbonButton(wx.Button, RibbonThemeMixin):
    """
    Button on a FrameRibbon.

    Parameters
    ----------
    parent : FrameRibbonSection
        Section containing this button
    label : str
        Label to display on this button
    icon : str
        Stem of icon to use for this button
    tooltip : str
        Tooltip to display on hover
    callback : function
        Function to call when this button is clicked
    style : int
        Combination of wx button styles to apply
    """
    def __init__(
            self, 
            parent, 
            label, 
            icon=None, 
            tooltip="", 
            callback=None, 
            style=wx.BU_NOTEXT
        ):
        # figure out width
        w = -1
        if style | wx.BU_NOTEXT == style:
            w = 40
        # initialize
        wx.Button.__init__(self, parent, style=wx.BORDER_NONE | style, size=(w, 44))
        self.SetMinSize((40, 44))
        # set label
        self.SetLabelText(label)
        # set tooltip
        if tooltip and style | wx.BU_NOTEXT == style:
            # if there's no label, include it in the tooltip
            tooltip = f"{label}: {tooltip}"
        self.SetToolTip(tooltip)
        # set icon
        self.SetIcon(icon)
        # inherit theme
        self.InheritTheme()
        # if given, bind callback
        if callback is not None:
            self.Bind(wx.EVT_BUTTON, callback)
        # setup hover behaviour
        self.Bind(wx.EVT_ENTER_WINDOW, self.onHover)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.onHover)
    
    def SetIcon(self, icon):
        """
        Set the icon for this button (will update with theme).

        Parameters
        ----------
        icon : wx_ribbon.icons.RibbonIcon
            RibbonIcon object containing both light and dark versions of this icon.
        """
        self.icon = icon
    
    def ApplyTheme(self):
        RibbonThemeMixin.ApplyTheme(self)
        # also update icon
        self.SetBitmap(
            self.icon.GetBitmap(height=28, style=self.theme.icons),
            dir=wx.TOP
        )
        self.SetBitmapMargins(8, 8)

        self.Update()
        self.Refresh()

    def onHover(self, evt):
        if evt.EventType == wx.EVT_ENTER_WINDOW.typeId:
            # on hover, lighten background
            self.SetBackgroundColour(self.theme.mantle)
        else:
            # otherwise, keep same colour as parent
            self.SetBackgroundColour(self.theme.crust)


class FrameRibbonDropdownButton(wx.Panel, RibbonThemeMixin):
    def __init__(self, parent, label, icon=None, callback=None, menu=None):
        wx.Panel.__init__(self, parent)
        # inherit theme
        self.InheritTheme()
        # setup sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        # make button
        self.button = wx.Button(self, label=label, style=wx.BORDER_NONE)
        self.sizer.Add(self.button, proportion=1, border=0, flag=wx.EXPAND | wx.ALL)
        # set icon
        self._icon = icons.ButtonIcon(icon, size=32)
        # bind button callback
        if callback is not None:
            self.button.Bind(wx.EVT_BUTTON, callback)

        # make dropdown
        self.drop = wx.Button(self, label="▾", style=wx.BU_EXACTFIT | wx.BORDER_NONE)
        self.sizer.Add(self.drop, border=0, flag=wx.EXPAND | wx.ALL)
        # bind menu
        self.drop.Bind(wx.EVT_BUTTON, self.onMenu)
        self.menu = menu

        # setup hover behaviour
        self.button.Bind(wx.EVT_ENTER_WINDOW, self.onHover)
        self.button.Bind(wx.EVT_LEAVE_WINDOW, self.onHover)
        self.drop.Bind(wx.EVT_ENTER_WINDOW, self.onHover)
        self.drop.Bind(wx.EVT_LEAVE_WINDOW, self.onHover)

    def onMenu(self, evt):
        menu = self.menu
        # skip if there's no menu
        if menu is None:
            return
        # if menu is created live, create it
        if callable(menu):
            menu = menu(self, evt)
        # show menu
        self.PopupMenu(menu)

    def _applyAppTheme(self):
        # set color
        for obj in (self, self.button, self.drop):
            obj.SetBackgroundColour(colors.app['frame_bg'])
            obj.SetForegroundColour(colors.app['text'])
        # set bitmaps again
        self._icon.reload()
        self.button.SetBitmap(self._icon.bitmap)
        self.button.SetBitmapCurrent(self._icon.bitmap)
        self.button.SetBitmapPressed(self._icon.bitmap)
        self.button.SetBitmapFocus(self._icon.bitmap)
        # refresh
        self.Refresh()

    def onHover(self, evt):
        if evt.EventType == wx.EVT_ENTER_WINDOW.typeId:
            # on hover, lighten background
            evt.EventObject.SetBackgroundColour(colors.app['panel_bg'])
        else:
            # otherwise, keep same colour as parent
            evt.EventObject.SetBackgroundColour(colors.app['frame_bg'])


EVT_RIBBON_SWITCH = wx.PyEventBinder(wx.IdManager.ReserveId())


class FrameRibbonSwitchCtrl(wx.Panel, RibbonThemeMixin):
    """
    A switch with two modes. Use `addDependency` to make presentation of other buttons
    conditional on this control's state.
    """
    def __init__(
            self, parent, labels=("", ""), startMode=0,
            callback=None,
            style=wx.HORIZONTAL
    ):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        # inherit theme
        self.InheritTheme()
        # use style tag to get text alignment and control orientation
        alignh = style & (wx.BU_LEFT | wx.BU_RIGHT)
        alignv = style & (wx.BU_TOP | wx.BU_BOTTOM)
        alignEach = [alignh | alignv, alignh | alignv]
        orientation = style & (wx.HORIZONTAL | wx.VERTICAL)
        # if orientation is horizontal and no h alignment set, wrap text around button
        if orientation == wx.HORIZONTAL and not alignh:
            alignEach = [wx.BU_RIGHT | alignv, wx.BU_LEFT | alignv]
        # setup sizers
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)
        self.btnSizer = wx.BoxSizer(orientation)
        # setup depends dict
        self.depends = []
        # make icon
        self.icon = wx.Button(self, style=wx.BORDER_NONE | wx.BU_NOTEXT | wx.BU_EXACTFIT)
        self.icon.Bind(wx.EVT_BUTTON, self.onModeToggle)
        self.icon.Bind(wx.EVT_ENTER_WINDOW, self.onHover)
        self.icon.Bind(wx.EVT_LEAVE_WINDOW, self.onHover)
        # make switcher buttons
        self.btns = []
        for i in range(2):
            btn = wx.Button(
                self, label=labels[i], size=(-1, 16),
                style=wx.BORDER_NONE | wx.BU_EXACTFIT | alignEach[i]
            )
            if style & wx.BU_NOTEXT:
                btn.Hide()
            self.btnSizer.Add(btn, proportion=orientation == wx.VERTICAL, flag=wx.EXPAND)
            btn.Bind(wx.EVT_BUTTON, self.onModeSwitch)
            btn.Bind(wx.EVT_ENTER_WINDOW, self.onHover)
            btn.Bind(wx.EVT_LEAVE_WINDOW, self.onHover)
            self.btns.append(btn)
        # arrange icon/buttons according to style
        self.sizer.Add(self.btnSizer, proportion=1, border=3, flag=wx.EXPAND | wx.ALL)
        params = {'border': 6, 'flag': wx.EXPAND | wx.ALL}
        if orientation == wx.HORIZONTAL:
            # if horizontal, always put icon in the middle
            self.btnSizer.Insert(1, self.icon, **params)
        elif alignh == wx.BU_LEFT:
            # if left, put icon on left
            self.sizer.Insert(0, self.icon, **params)
        else:
            # if right, put icon on right
            self.sizer.Insert(1, self.icon, **params)
        # make icons
        if orientation == wx.HORIZONTAL:
            stems = ["switchCtrlLeft", "switchCtrlRight"]
            size = (32, 16)
        else:
            stems = ["switchCtrlTop", "switchCtrlBot"]
            size = (16, 32)
        self.icons = [
            icons.ButtonIcon(stem, size=size) for stem in stems
        ]
        # set starting mode
        self.setMode(startMode, silent=True)
        # bind callback
        if callback is not None:
            self.Bind(EVT_RIBBON_SWITCH, callback)

        self.Layout()

    def onModeSwitch(self, evt):
        evtBtn = evt.GetEventObject()
        # iterate through switch buttons
        for mode, btn in enumerate(self.btns):
            # if button matches this event...
            if btn is evtBtn:
                # change mode
                self.setMode(mode)

    def onModeToggle(self, evt=None):
        if self.mode == 0:
            self.setMode(1)
        else:
            self.setMode(0)

    def setMode(self, mode, silent=False):
        # set mode
        self.mode = mode
        # iterate through switch buttons
        for btnMode, btn in enumerate(self.btns):
            # if it's the correct button...
            if btnMode == mode:
                # style accordingly
                btn.SetForegroundColour(colors.app['text'])
            else:
                btn.SetForegroundColour(colors.app['rt_timegrid'])
        # set icon
        self.icon.SetBitmap(self.icons[mode].bitmap)

        # handle depends
        for depend in self.depends:
            # get linked ctrl
            ctrl = depend['ctrl']
            # show/enable according to mode
            if depend['action'] == "show":
                ctrl.Show(mode == depend['mode'])
            if depend['action'] == "enable":
                ctrl.Enable(mode == depend['mode'])
        # emit event
        if not silent:
            evt = wx.CommandEvent(EVT_RIBBON_SWITCH.typeId)
            evt.SetInt(mode)
            evt.SetString(self.btns[mode].GetLabel())
            wx.PostEvent(self, evt)
        # refresh
        self.Refresh()
        self.Update()
        self.GetTopLevelParent().Layout()

    def onHover(self, evt):
        if evt.EventType == wx.EVT_ENTER_WINDOW.typeId:
            # on hover, lighten background
            evt.EventObject.SetForegroundColour(colors.app['text'])
        else:
            # otherwise, keep same colour as parent
            if evt.EventObject is self.btns[self.mode]:
                evt.EventObject.SetForegroundColour(colors.app['text'])
            else:
                evt.EventObject.SetForegroundColour(colors.app['rt_timegrid'])

    def addDependant(self, ctrl, mode, action="show"):
        """
        Connect another button to one mode of this ctrl such that it is shown/enabled only when
        this ctrl is in that mode.

        Parameters
        ----------
        ctrl : wx.Window
            Control to act upon
        mode : str
            The mode in which to show/enable the linked ctrl
        action : str
            One of:
            - "show" Show the control
            - "enable" Enable the control
        """
        self.depends.append(
            {
                'mode': mode,  # when in mode...
                'action': action,  # then...
                'ctrl': ctrl,  # to...
            }
        )