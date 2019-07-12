import tkinter as tk
from tkinter import ttk
from tkinter import N, S, E, W  # sticky Constants
from tkinter import messagebox

APP_NAME = 'Freighter Planner'

# Arbitrarily large number for grid columns/rows used to position widgets at
# the bottom or right-most part of the grid. Essentially the opposite of 0.
LAST_ROWCOL = 999

# TODO: ttk.Notebook doesn't seem to support dragging tabs to re-order them...
class TabPane(ttk.Notebook):
  """Tabbed container for other components."""

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

    self.frames = [ttk.Frame(self)]
    self.add(self.frames[0])

  def get_tab_child(self, tab_id):
    return self.winfo_children()[self.index(tab_id)]


class StatusBar(ttk.Frame):
  """Window status bar"""

  _windows_with_statusbar = set()

  def __init__(self, window, *args, **kwargs):
    if (window in self._windows_with_statusbar):
      raise Exception(f'Cannot add more than one StatusBar to window {window!r}')
    else:
      self._windows_with_statusbar.add(window)
    super().__init__(window, *args, **kwargs)

    window.columnconfigure(0, weight=1)
    window.rowconfigure(LAST_ROWCOL, weight=1)
    self.configure(relief=tk.SUNKEN, borderwidth=2)
    self.grid(row=LAST_ROWCOL, columnspan=LAST_ROWCOL, sticky=(S, E, W))

    ttk.Label(self, text='foobar').grid()


class Menu(tk.Menu):
  """Menu entry for a MenuBar or as a submenu of another Menu.

  Wrapper class for a cascaded menu providing convenient accessors and
  methods."""

  def __init__(self, parent, label: str, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)
    self.label = label


  def add_to_parent_menu(self, *args, **kwargs):
    """Adds the menu to its parent menu via add_cascade() with any arguments
    passed along to it."""

    self.master.add_cascade(*args, label=self.label, menu=self, **kwargs)


class MenuBar(tk.Menu):
  """Menu bar for the application."""

  def __init__(self, window, *args, **kwargs):
    super().__init__(window, *args, **kwargs)
    window['menu'] = self

    self.menus = {}
    for name in ('File', 'Edit', 'View', 'Help'):
      self.menus[name] = Menu(self, name)
      self.add_cascade(label=name, menu=self.menus[name], underline=0)

    # TODO: Most of these need their commands written and set
    # TODO: Mac-specific accelerators

    # File
    f = self.menus['File']
    f.add_command(label='New Plan', command=new_plan, accelerator='Ctrl+N', underline=0)
    f.add_command(label='Open Plan...', command=open_plan, accelerator='Ctrl+O', underline=0)

    recent = Menu(f, 'Open Recent')
    recent.add_to_parent_menu(underline=5)
    # TODO: Disable this entry when there's no recently closed plan
    recent.add_command(label='Reopen Closed Plan', accelerator='Ctrl+Shift+T', underline=0)
    recent.add_separator()
    # TODO: recent files go here, with numbers underlined
    recent.add_command(label='No Recent Plan', state='disabled')
    recent.add_separator()
    # TODO: Disable this entry when there are no recent plans
    recent.add_command(label='Clear Recent Plans', underline=0)

    f.add_command(label='Close Plan', accelerator='Ctrl+W', underline=0)
    f.add_separator()
    f.add_command(label='Save Plan', accelerator='Ctrl+S', underline=0)
    f.add_command(label='Save Plan As...', accelerator='Ctrl+Shift+S', underline=10)
    f.add_separator()
    f.add_command(label='Exit', command=window.exit, underline=1)

    # Edit
    e = self.menus['Edit']
    e.add_command(label='Undo', accelerator='Ctrl+Z', underline=0)
    e.add_command(label='Redo', accelerator='Ctrl+Y', underline=0)
    e.add_separator()
    e.add_command(label='Cut', accelerator='Ctrl+X', underline=2)
    e.add_command(label='Copy', accelerator='Ctrl+C', underline=0)
    e.add_command(label='Paste', accelerator='Ctrl+V', underline=0)
    e.add_separator()
    e.add_command(label='Preferences...', accelerator='Ctrl+P', underline=3)

    # View
    v = self.menus['View']
    v.add_checkbutton(label='Show Grid', underline=5) # TODO

    # Help
    h = self.menus['Help']
    h.add_separator()
    # TODO: Show usual information; View License "link" that opens a popup, etc.
    h.add_command(label=f'About {APP_NAME}', underline=0) # TODO


# NOTE: Will likely need to implement this as a canvas
class Editor(ttk.Frame):
  """Frame containing the editing area.

  Contains the grid space representing the floor layout of the freighter.
  """

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)


# TBD: Design of the palette
# Simple grid layout with every component, analogous to a color palette? (meh)
# Ideally grouped in some way: sections or as cascading buttons
#   - Sections acting as clusters
#   - Cascading buttons (ttk.Menubutton) that expand into relevant, more
#     specific components i.e. one for corridor pieces, another for rooms, etc.
#   - Mimic the in-game structure of the components in the GUI?
class Palette(ttk.Frame):
  """Frame containing the freighter components palette."""

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)


class Sidebar(ttk.Frame):
  """Frame acting as the sidebar; holds component breakdown information.

  Shows component counts, their material costs, etc."""

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)

  # create tab bar (All floors, current floor only, etc.)
  # interface scrolls as more component types are in use
  # each "cell" should probably be a class object


class FloorManager(ttk.Frame):
  """Frame containing the floor manager.

  Displays a list of added floors, with visibility toggles and the like.
  Not much unlike the layers component in a graphics editor."""

  def __init__(self, parent, *args, **kwargs):
    super().__init__(parent, *args, **kwargs)


class MainApplication(tk.Tk):
  """Top-most window, holding all components; the entire application."""

  def __init__(self):
    super().__init__()
    self.option_add('*tearOff', False) # Disable tear-off menus
    self.protocol('WM_DELETE_WINDOW', self.exit)

    self.title(APP_NAME)

    self.menubar = MenuBar(self)
    self.configure(menu=self.menubar)

    self.splitpane = ttk.PanedWindow(self, orient=tk.VERTICAL)
    self.splitpane.grid()
    self.sidebar = Sidebar(self.splitpane, width=200)
    self.sidebar.grid(row=0, column=0, rowspan=LAST_ROWCOL, sticky=(N, S, E, W))
    self.editor = Editor(self.splitpane)
    self.editor.grid(row=0, column=1, rowspan=LAST_ROWCOL, sticky=(N, S, E, W))

    # self.tabpane = TabPane(self)
    # self.tabpane.grid(row=0, column=1)

    self.statusbar = StatusBar(self)

  def exit(self):
    # TODO: Do everything needed to close gracefully, e.g.
    #   - Prompt to save unsaved plans
    #   - anything else
    # TODO: Create a custom save-before-quit dialog, e.g. Save, Don't Save, Cancel
    # if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
    self.destroy()


def new_plan():
  pass


def open_plan():
  pass

# TBD: Where to put this?
app = MainApplication()
app.mainloop()