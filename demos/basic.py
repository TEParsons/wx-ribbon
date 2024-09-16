"""
This demo shows how to make a basic toolbar with some common controls.
"""

import wx
from wx_ribbon import FrameRibbon, themes, icons


class DemoAppFrame(wx.Frame):
    """
    A basic frame to demonstrate how to use wx_ribbon tools.
    """
    def __init__(self, parent=None, size=(1080, 720)):
        # initialise base class
        wx.Frame.__init__(
            self,
            parent=parent,
            size=size
        )
        # setup sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        # make ribbon
        self.ribbon = FrameRibbon(
            self,
            theme=themes.RB_THEME_LIGHT
        )
        self.sizer.Add(self.ribbon, flag=wx.EXPAND)
        self.populate_ribbon()
        # add panel for page contents
        panel = wx.Panel(self)
        self.sizer.Add(panel, proportion=1, flag=wx.EXPAND)
    
    def populate_ribbon(self):
        """
        Populate this frame's ribbon with buttons.
        """
        # add a "File" section with some common controls
        self.ribbon.AddSection(
            name="file",
            label="File",
            icon=icons.RB_ICON_FILE_OPEN
        )
        self.ribbon.AddButton(
            section="file",
            name="file_new",
            label="New",
            tooltip=self.on_file_new.__doc__,
            callback=self.on_file_new,
            icon=icons.RB_ICON_FILE_NEW
        )
        self.ribbon.AddButton(
            section="file",
            name="file_save",
            label="Save",
            tooltip=self.on_file_save.__doc__,
            callback=self.on_file_save,
            icon=icons.RB_ICON_FILE_SAVE
        )
        self.ribbon.AddButton(
            section="file",
            name="file_open",
            label="Open",
            tooltip=self.on_file_open.__doc__,
            callback=self.on_file_open,
            icon=icons.RB_ICON_FILE_OPEN
        )
        self.ribbon.AddSeparator()

        # add an "Edit" section with some common controls
        self.ribbon.AddSection(
            name="edit",
            label="Edit",
            icon=icons.RB_ICON_EDIT
        )
        self.ribbon.AddButton(
            section="edit",
            name="copy",
            label="Copy",
            tooltip=self.on_edit_copy.__doc__,
            callback=self.on_edit_copy,
            icon=icons.RB_ICON_COPY
        )
        self.ribbon.AddButton(
            section="edit",
            name="paste",
            label="Paste",
            tooltip=self.on_edit_paste.__doc__,
            callback=self.on_edit_paste,
            icon=icons.RB_ICON_PASTE
        )
        self.ribbon.AddButton(
            section="edit",
            name="undo",
            label="Undo",
            tooltip=self.on_edit_undo.__doc__,
            callback=self.on_edit_undo,
            icon=icons.RB_ICON_UNDO
        )
        self.ribbon.AddButton(
            section="edit",
            name="redo",
            label="Redo",
            tooltip=self.on_edit_redo.__doc__,
            callback=self.on_edit_redo,
            icon=icons.RB_ICON_REDO
        )

        # add section for editing the current project
        self.ribbon.AddSeparator()
        self.ribbon.AddSection(
            name="project",
            label="Project",
            icon=icons.RB_ICON_INFO
        )
        self.ribbon.AddButton(
            section="project",
            name="settings",
            label="Settings", 
            tooltip=self.on_project_settings.__doc__,
            callback=self.on_project_settings,
            icon=icons.RB_ICON_SETTINGS
        )
        self.ribbon.AddButton(
            section="project",
            name="info",
            label="TEParsons/wx-self.ribbon", 
            tooltip=self.on_project_info.__doc__,
            callback=self.on_project_info,
            icon=icons.RB_ICON_INFO, 
            style=wx.BU_LEFT  # this button has a label!
        )

        # add section for running stuff to show off the switch ctrl
        self.ribbon.AddSeparator()
        self.ribbon.AddSection(
            name="run",
            label="Run",
            icon=icons.RB_ICON_PLAY
        )
        switch = self.ribbon.AddSwitchCtrl(
            section="run",
            name="mode",
            labels=("Run", "Debug"),
            startMode=0,
            callback=self.on_run_mode,
            style=wx.HORIZONTAL
        )
        run = self.ribbon.AddButton(
            section="run",
            name="run",
            label="Run",
            tooltip=self.on_run_run.__doc__,
            callback=self.on_run_run,
            icon=icons.RB_ICON_PLAY
        )
        switch.AddDependant(run, 0, action="enable")  # adding buttons as "dependents" to a switch ctrl will enable/disable them according to its state
        debug = self.ribbon.AddButton(
            section="run",
            name="debug",
            label="Debug",
            tooltip=self.on_run_debug.__doc__,
            callback=self.on_run_debug,
            icon=icons.RB_ICON_BUG
        )
        switch.AddDependant(debug, 1, action="enable")

        # add section for user switching control - this one doesn't have a label, and is off to the right
        self.ribbon.AddSeparator()
        self.ribbon.AddStretchSpacer()
        self.ribbon.AddSection(
            name="user",
        )
        # we need to create a menu for the dropdown to open when clicked...
        self.user_menu = wx.Menu()
        switch_user = self.user_menu.Append(wx.ID_ANY, item="Switch user...")
        self.user_menu.Bind(wx.EVT_MENU, self.on_user_switch, source=switch_user)
        log_out = self.user_menu.Append(wx.ID_ANY, item="Log out")
        self.user_menu.Bind(wx.EVT_MENU, self.on_user_logout, source=log_out)
        self.ribbon.AddDropdownButton(
            section="user",
            name="user",
            label="TEParsons",
            callback=self.on_user_info, 
            menu=self.user_menu,
            icon=icons.RB_ICON_USER,
        )
        # layout
        self.ribbon.Layout()
    
    # file section callbacks
    
    def on_file_new(self, evt=None):
        """
        Create a new file.
        """
        print("PRESSED", "File New")
    
    def on_file_save(self, evt=None):
        """
        Save the current file.
        """
        print("PRESSED", "File Save")
    
    def on_file_open(self, evt=None):
        """
        Open an existing file.
        """
        print("PRESSED", "File Open")
    
    # edit section callbacks
    
    def on_edit_copy(self, evt=None):
        """
        Copy selected content to the clipboard.
        """
        print("PRESSED", "Edit Copy")
    
    def on_edit_paste(self, evt=None):
        """
        Paste contents of the clipboard at selection.
        """
        print("PRESSED", "Edit Paste")
    
    def on_edit_undo(self, evt=None):
        """
        Undo the last action.
        """
        print("PRESSED", "Edit Undo")
    
    def on_edit_redo(self, evt=None):
        """
        Redo the last undone action.
        """
        print("PRESSED", "Edit Redo")
    
    # project section callbacks

    def on_project_settings(self, evt=None):
        """
        Edit settings for the current project.
        """
        print("PRESSED", "Project Settings")
    
    def on_project_info(self, evt=None):
        """
        View info for the current project.
        """
        print("PRESSED", "Project Info")
        # open the wx-ribbon project in browser
        import webbrowser
        webbrowser.open("https://github.com/TEParsons/wx-ribbon")
    
    # run section callbacks

    def on_run_mode(self, evt=None):
        """
        Set the run mode (run or debug)
        """
        # get selection (integer)
        mode = evt.GetInt()
        # get selection (string)
        mode_str = evt.GetString()
        
        print("TOGGLED", "Run Mode", mode_str)

    def on_run_run(self, evt=None):
        """
        Run the current file.
        """
        print("PRESSED", "Run Run")
    
    def on_run_debug(self, evt=None):
        """
        Run the current file in debug mode.
        """
        print("PRESSED", "Run Debug")
    
    def on_user_info(self, evt=None):
        """
        View info about the current user.
        """
        print("PRESSED", "User Info")
        # open my GitHub in browser
        import webbrowser
        webbrowser.open("https://github.com/TEParsons")
    
    def on_user_switch(self, evt=None):
        """
        Change which user you are logged in as.
        """
        print("PRESSED", "User Switch")
    
    def on_user_logout(self, evt=None):
        """
        Log out as the current user.
        """
        print("PRESSED", "User Logout")


if __name__ == "__main__":
    # make a basic wx app
    app = wx.App()
    # add demo frame
    frame = DemoAppFrame()
    frame.Show()
    # start app
    app.MainLoop()
