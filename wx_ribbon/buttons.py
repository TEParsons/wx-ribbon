import wx
import sys
import logging
from wx_ribbon import ribbon, themes, icons
from wx_ribbon.themes.base import RibbonThemeMixin


class FrameRibbonButtonMeta:
    def __init_subclass__(cls):
        cls_name = cls.__name__.replace("FrameRibbon", "")
        fcn_name = f"Add{cls_name}"

        # define function to create the given button from a section
        def _createButton(self, name, *args, **kwargs):
            # create the button
            btn = cls(self, *args, **kwargs)
            # store references
            self.buttons[name] = self.ribbon.buttons[name] = btn
            # add button to sizer
            flags = wx.EXPAND
            if sys.platform == "darwin":
                # add top padding on Mac
                flags |= wx.TOP
            self.sizer.Add(btn, border=12, flag=flags)

            return btn
        
        # assign method to FrameRibbonSection
        setattr(ribbon.FrameRibbonSection, fcn_name, _createButton)
        _createButton.__doc__ = cls.__doc__
        logging.debug(
            f"Assigned method {fcn_name} (creates a {cls.__name__}) to FrameRibbonSection"
        )
        # define function to create the given button from the ribbon
        def _createButton(self, section, name, *args, **kwargs):
            # if section doesn't exist, make it
            if section not in self.sections:
                self.AddSection(section, label=section)
            # call addButton method from given section
            btn = getattr(self.sections[section], fcn_name)(
                name, *args, **kwargs
            )

            return btn
        # assign method to FrameRibbon
        setattr(ribbon.FrameRibbon, fcn_name, _createButton)
        _createButton.__doc__ = cls.__doc__
        logging.debug(
            f"Assigned method {fcn_name} (creates a {cls.__name__}) to FrameRibbonSection"
        )


class FrameRibbonButton(wx.Button, FrameRibbonButtonMeta, RibbonThemeMixin):
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
        self.SetMinSize((w, 44))
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
        if self.icon is not None:
            self.SetBitmap(
                self.icon.GetBitmap(height=28, style=self.theme.icons)
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


class FrameRibbonDropdownButton(wx.Panel, FrameRibbonButtonMeta, RibbonThemeMixin):
    def __init__(self, parent, label, icon=None, callback=None, menu=None, style=wx.BU_LEFT):
        wx.Panel.__init__(self, parent)
        # setup sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        # make button
        self.button = FrameRibbonButton(
            self, 
            label=label,
            icon=icon,
            callback=callback,
            style=style
        )
        self.sizer.Add(self.button, proportion=1, border=0, flag=wx.EXPAND | wx.ALL)

        # make dropdown
        self.drop = wx.Button(
            self, 
            label="▾", 
            style=wx.BU_EXACTFIT | wx.BORDER_NONE
        )
        self.sizer.Add(self.drop, border=0, flag=wx.EXPAND | wx.ALL)
        # bind menu
        self.drop.Bind(wx.EVT_BUTTON, self.onMenu)
        self.menu = menu
        # inherit theme
        self.InheritTheme()

        # setup hover behaviour
        self.drop.Bind(wx.EVT_ENTER_WINDOW, self.onHover)
        self.drop.Bind(wx.EVT_LEAVE_WINDOW, self.onHover)
    
    def SetIcon(self, icon):
        """
        Set the icon for this button (will update with theme).

        Parameters
        ----------
        icon : wx_ribbon.icons.RibbonIcon
            RibbonIcon object containing both light and dark versions of this icon.
        """
        self.button.SetIcon(icon)
    
    def ApplyTheme(self):
        # make sure button has a theme
        self.button.InheritTheme()
        # use base theme method
        RibbonThemeMixin.ApplyTheme(self)
        # update background of drop button
        self.drop.SetBackgroundColour(self.theme.crust)
        self.drop.SetForegroundColour(self.theme.text)

        self.Update()
        self.Refresh()
    
    def onHover(self, evt):
        # get hover target
        target = evt.GetEventObject()

        if evt.EventType == wx.EVT_ENTER_WINDOW.typeId:
            # on hover, lighten background
            target.SetBackgroundColour(self.theme.mantle)
        else:
            # otherwise, keep same colour as parent
            target.SetBackgroundColour(self.theme.crust)   

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


EVT_RIBBON_SWITCH = wx.PyEventBinder(wx.IdManager.ReserveId())


class FrameRibbonSwitchCtrl(wx.Panel, FrameRibbonButtonMeta, RibbonThemeMixin):
    """
    A switch with two modes. Use `AddDependency` to make presentation of other buttons
    conditional on this control's state.
    """
    def __init__(
            self, parent, 
            labels=("", ""),
            startMode=0,
            callback=None,
            style=wx.HORIZONTAL
    ):
        wx.Panel.__init__(self, parent)
        self.parent = parent
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
            self.icons = [icons.RB_ICON_SWITCH_LEFT, icons.RB_ICON_SWITCH_RIGHT]
        else:
            self.icons = [icons.RB_ICON_SWITCH_TOP, icons.RB_ICON_SWITCH_BOTTOM]
        # inherit theme
        self.InheritTheme()
        # set starting mode
        self.SetMode(startMode, silent=True)
        # bind callback
        if callback is not None:
            self.Bind(EVT_RIBBON_SWITCH, callback)

        self.Layout()
    
    def ApplyTheme(self):
        # use base theme method
        RibbonThemeMixin.ApplyTheme(self)
        # update background of all buttons
        for btn in self.btns:
            btn.SetBackgroundColour(self.theme.crust)
        # update background of switch
        self.icon.SetBackgroundColour(self.theme.crust)

        self.Update()
        self.Refresh()
    
    def SetMode(self, mode, silent=False):
        # set mode
        self.mode = mode
        # iterate through switch buttons
        for btnMode, btn in enumerate(self.btns):
            # if it's the correct button...
            if btnMode == mode:
                # style accordingly
                btn.SetForegroundColour(self.theme.text)
            else:
                btn.SetForegroundColour(self.theme.MakeDisabled(self.theme.text))
        # set icon
        self.icon.SetBitmap(self.icons[mode].GetBitmap(height=28, style=self.theme.icons))

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

    def onModeSwitch(self, evt):
        evtBtn = evt.GetEventObject()
        # iterate through switch buttons
        for mode, btn in enumerate(self.btns):
            # if button matches this event...
            if btn is evtBtn:
                # change mode
                self.SetMode(mode)

    def onModeToggle(self, evt=None):
        if self.mode == 0:
            self.SetMode(1)
        else:
            self.SetMode(0)

    def onHover(self, evt):
        if evt.EventType == wx.EVT_ENTER_WINDOW.typeId:
            # on hover, lighten background
            evt.EventObject.SetForegroundColour(self.theme.text)
        else:
            # otherwise, keep same colour as parent
            col = wx.Colour(self.theme.text)
            if evt.EventObject is self.btns[self.mode]:
                evt.EventObject.SetForegroundColour(col)
            else:
                evt.EventObject.SetForegroundColour(self.theme.MakeDisabled(self.theme.text))
    
    def AddDependant(self, ctrl, mode, action="show"):
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
        # do action once now
        if action == "show":
            ctrl.Show(self.mode == mode)
        if action == "enable":
            ctrl.Enable(self.mode == mode)