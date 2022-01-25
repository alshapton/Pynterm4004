

import py_cui as cui
import sys
import os
from os.path import expanduser

# Import Pyntel4004 functionality
from hardware.processor import Processor
from assembler.assemble import assemble


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
    write a copy of the sample config to ~/.config/<config.NAME>/config.py
    """
    ensure_dir(os.path.expanduser(file_path))
    # replace with config path
    with open(os.path.expanduser(file_path), 'w', encoding='utf-8') as f:
        f.write("import py_cui\n"
                "# general\n"
                "WPP = None\n"
                "UNICODE = True\n"
                "STEP_SIZE = 30\n"
                "NAME = \"Pynterm4004\"\n"
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

def read_program(program_name: str):
    err = ''
    programcode = ''
    programcodearray = []

    try:
        program = open(program_name, 'r',  encoding='utf-8')  # noqa
    except IOError:
        err = ('FATAL: Pass 1: File "' + program_name +
               '" does not exist.')
        return err
    else:
        print()
        print()
        print('Program Code:', program_name)
        print()

        for _loop in range(3):
            programcodearray.append('')
        while True:
            line = program.readline()
            # if line is empty, end of file is reached
            if (not line) or (line == '') or len(line) == 0:
                # Completed reading program into memory
                break
            programcodearray.append(line.rstrip())
            programcode = programcode + line
        # Completed reading program into memory (or errored-out)
        program.close()
        return err, programcode, programcodearray



class MCS4:

    def __init__(self, master):
        """__init__.
        Args:
            master: py_cui root module
        """

        self.master = master
        self.scene = None
        self.active = list()
        self.step = config.STEP_SIZE

        # used for changing light and group color
        self.color_dict = config.COLOR_DICT
        self.colors = ["red", "blue", "green", "purple", "teal"]

        # set unicode borders
        if config.UNICODE:
            self.master.toggle_unicode_borders()

        err, programcode, programcodearray = read_program(program_name)

        # Add main text block for editor text.
        self.program = self.master.add_text_block(
            'Program: ' + program_name, 0, 0, row_span=2, column_span=2,
            padx=1, pady=0, initial_text=programcode)

        # Add block for program debugger.
        self.runprogram = \
            self.master.add_scroll_menu('Run', 2, 0, row_span=3,
                                        column_span=2,  padx=1, pady=0)
        self.runprogram.add_item_list(programcodearray)
        # Bind the 'ENTER' key to the "Next Line" function
        self.runprogram.add_key_command(cui.keys.KEY_ENTER,
                                        self.set_title_from_menu)

        self.registers = \
            self.master.add_block_label('Registers\n Accumulator = 0', 0,
                                        2, row_span=2,
                                        column_span=2, padx=1, pady=-1,
                                        center=False)
        self.registers.toggle_border()
        self.registers.set_selectable(False)

        # add help text for program statusbar
        self.program.set_help_text("Arrow keys to navigate, ESC to exit")
        self.runprogram.set_help_text("ENTER to run next line, ESC to exit")

        # adding items to each menu

        self.master.set_widget_cycle_key(cui.keys.KEY_TAB)
        self.master.status_bar.set_color(config.STATUSBAR_COLOR)
        self.master.title_bar.set_color(config.TITLEBAR_COLOR)

    # Function that sets the root window title
    def set_title_from_menu(self):
        root.set_title(self.runprogram.get())
        self.registers.set_title(self.runprogram.get())

# change config path here if needed
CONFIG_PATH = "~/.config/Pynterm4004/config.py"
HOME = expanduser("~")
ensure_dir(f"{HOME}/.config/Pyterm4004/")
# add config to python path and import
sys.path.append(os.path.dirname(os.path.expanduser(CONFIG_PATH)))
# check if config file exists if not write sample
try:
    import config
except Exception:
    copy_config(CONFIG_PATH)
    print("Config file created. Please start Pynterm4004 again.")
    sys.exit(0)

program_name = 'examples/example2.asm'

root = cui.PyCUI(8, 8)
root.set_title(config.NAME)
Main = MCS4(root)
root.start()
