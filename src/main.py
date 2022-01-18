

import py_cui as cui
import sys
import os
from os.path import expanduser

# some general functions to run before the TUI starts
def ensure_dir(file_path):
    """ensure_dir.
    makes sure that directory exists and creates one should
    the directory not exist
    Args:
        file_path: path to file
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def copy_config(file_path):
    """copy_config.
    write a copy of the sample config to ~/.config/hue-tui/config.py
    """
    ensure_dir(os.path.expanduser(file_path))
    # replace with config path
    with open(os.path.expanduser(file_path), 'w', encoding='utf-8') as f:
        f.write("import py_cui\n"
                "# general\n"
                "WPP = None\n"
                "UNICODE = True\n"
                "STEP_SIZE = 30\n"
                "# colors\n"
                "COLOR = py_cui.WHITE_ON_BLACK\n"
                "SELECTED_COLOR = py_cui.CYAN_ON_BLACK\n"
                "BORDER_COLOR = py_cui.BLUE_ON_BLACK\n"
                "LOGO_COLOR = py_cui.CYAN_ON_BLACK\n"
                "STATUSBAR_COLOR = py_cui.BLACK_ON_WHITE\n"
                "TITLEBAR_COLOR = py_cui.BLACK_ON_WHITE\n"
                "# dict for preset hue colors\n"
                "COLOR_DICT = {\n"
                "   \"red\": \"#DE3838\",\n"
                "   \"blue\": \"#2122E2\",\n"
                "   \"green\": \"#2EF615\",\n"
                "   \"purple\": \"#5c0099\",\n"
                "   \"teal\": \"#26F0C9\"\n"
                "}\n")



class MCS4:
    def __init__(self, master):
        """__init__.
        Args:
            master: py_cui root module
        """
        self.master = master
        self.scene = None
        self.bridge = []  # bridge info array
        self.active = list()
        self.step = config.STEP_SIZE
        self.disco = False
        self.WALL = None
        # used for changing light and group color
        self.color_dict = config.COLOR_DICT
        self.colors = ["red", "blue", "green", "purple", "teal"]

        # will be added when fixed
        # self.border_selected_color = None
        # set unicode borders
        if config.UNICODE:
            self.master.toggle_unicode_borders()
        # add banner
        self.logo = self.master.add_block_label(
            str(self.get_logo_text()), 0, 0, 1, 2)

        # items for each menu
        self.lights = 'X'
        self.groups = 'X'
        self.scenes = 'X'
        # creating each menu
        self.lights_menu = self.master.add_scroll_menu("Lights", 1, 0, 2, 2)
        self.groups_menu = self.master.add_scroll_menu("Groups", 3, 0, 2, 2)
        self.scenes_menu = self.master.add_scroll_menu("Scenes", 1, 2, 2, 2)
        self.active_box = self.master.add_scroll_menu("Active", 3, 2, 2, 2)
        # add active lights and groups to self.active
        # this also inits self.active_box with text
        self.active_box.set_selectable(False)
        self.bridge_information = self.master.add_scroll_menu(
            "Hue Bridge", 0, 2, 1, 2)
        self.xdrb_random = self.master.add_button("random XRDB colors",
                                                  5,
                                                  0,
                                                  1,
                                                  2,
                                                  command='fred')
        self.wallpaper_color = self.master.add_button(
            "wallpaper colors", 5, 2, 1, 2, command='fred')
        # add help text for statusbar
        self.lights_menu.set_help_text("Lights: arrow keys to navigate,"
                                       " j and k to change brightness,"
                                       " c to set color,"
                                       " d for disco mode, ENTER to toggle,"
                                       " ESC to exit")
        self.groups_menu.set_help_text("Groups: arrow keys to navigate,"
                                       " j and k to change brightness,"
                                       " c to set color,"
                                       " ENTER to toggle, ESC to exit")
        self.scenes_menu.set_help_text("Scenes: arrow keys to navigate,"
                                       " ENTER to select,"
                                       " ESC to exit")
        # adding items to each menu
        self.lights_menu.add_item_list(self.lights)
        self.groups_menu.add_item_list(self.groups)
        self.scenes_menu.add_item_list(self.scenes)
        self.bridge_information.add_item_list(self.bridge)

        self.master.set_widget_cycle_key(cui.keys.KEY_TAB)
        # adding keycommands
        # LIGHTS
        self.lights_menu.add_key_command(cui.keys.KEY_ENTER, 'fred')
        #self.lights_menu.add_key_command(cui.keys.KEY_K_LOWER,
                                         #command=self.inc_light_bri)
        #self.lights_menu.add_key_command(cui.keys.KEY_J_LOWER,
                                         #command=self.dec_light_bri)
        #self.lights_menu.add_key_command(cui.keys.KEY_D_LOWER,
                                         #self.disco_toggle)
        #self.lights_menu.add_key_command(cui.keys.KEY_C_LOWER,
                                         #self.light_color_popup)

        # GROUPS
        self.groups_menu.add_key_command(cui.keys.KEY_ENTER, 'fred')
        #self.groups_menu.add_key_command(cui.keys.KEY_K_LOWER,
                                         #self.inc_group_bri)
        #self.groups_menu.add_key_command(cui.keys.KEY_J_LOWER,
                                         #self.dec_group_bri)
        #self.groups_menu.add_key_command(cui.keys.KEY_C_LOWER,
                                         #self.group_color_popup)
        # setup colors
        #for key in self.master._widgets.keys():
        #    self.master.get_widgets()[key].set_color(config.COLOR)
        #    self.master.get_widgets()[key].set_selected_color(
        #        config.SELECTED_COLOR)
        #    self.master.get_widgets()[key].set_border_color(
        #        config.BORDER_COLOR)
            # broken for some reason
            # self.master.get_widgets()[key].set_focus_border_color(config.BORDER_SELECTED_COLOR)
        self.logo.set_color(config.LOGO_COLOR)
        self.master.status_bar.set_color(config.STATUSBAR_COLOR)
        self.master.title_bar.set_color(config.TITLEBAR_COLOR) 

    def get_logo_text(self):
        """get_logo_text.
            makes the logo banner with linebreaks
        """
        # make banner

        logo = '██╗  ██╗██╗   ██╗███████╗              ████████╗██╗   ██╗██╗\n'
        logo = logo + '██║  ██║██║   ██║██╔════╝              ╚══██╔══╝██║   ██║██║\n'
        logo = logo + '███████║██║   ██║█████╗      █████╗       ██║   ██║   ██║██║\n'
        logo = logo + '██╔══██║██║   ██║██╔══╝      ╚════╝       ██║   ██║   ██║██║\n'
        logo = logo + '██║  ██║╚██████╔╝███████╗                 ██║   ╚██████╔╝██║\n'
        logo = logo + '╚═╝  ╚═╝ ╚═════╝ ╚══════╝                 ╚═╝    ╚═════╝ ╚═╝\n'

        return logo

# change config path here if needed
CONFIG_PATH = "~/.config/Pynterm4004/config.py"
HOME = expanduser("~")
ensure_dir(f"{HOME}/.config/Pyterm400/")
# add config to python path and import
sys.path.append(os.path.dirname(os.path.expanduser(CONFIG_PATH)))
# check if config file exists if not write sample
try:
    import config
except Exception:
    copy_config(CONFIG_PATH)
    print("Config file created. Please start huetui again.")
    sys.exit(0)

root = cui.PyCUI(6, 4)
root.set_title("MCS-4")
Main = MCS4(root)
root.start()
