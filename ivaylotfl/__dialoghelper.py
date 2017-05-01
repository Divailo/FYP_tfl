from Tkinter import Tk  # gui library
import tkFileDialog  # file dialog library
from tkMessageBox import showerror, showinfo
import os.path

folderpath = ''


def open_dialog_and_gain_focus():
    # Make a top-level instance and hide since it is ugly and big.
    root = Tk()
    root.withdraw()

    # Make it almost invisible - no decorations, 0 size, top left corner.
    root.overrideredirect(True)
    root.geometry('0x0+0+0')

    # Show window again and lift it to top so it can get focus,
    # otherwise dialogs will end up behind the terminal.
    root.deiconify()
    root.lift()
    root.focus_force()
    return root


def destroy_root_view(view):
    view.destroy()



def show_error_box_with_message(message):
    Tk().withdraw()
    showerror('Error', message)


def show_info_box_with_message(message):
    Tk().withdraw()
    showinfo('Extraction done', message)


# initializes a file chooser to load the desired model
def ask_for_model():
    root = open_dialog_and_gain_focus()
    FILE_DIALOG_OPTIONS = {'filetypes': [('PTV Vissim network files', '*.inpx'), ('All files', '*.*')],
                           'title': 'Choose VISSIM model'}
    filename = tkFileDialog.askopenfilename(
        **FILE_DIALOG_OPTIONS)  # show an "Open" dialog box and return the path to the selected file
    global folderpath
    folderpath = filename
    destroy_root_view(root)
    return filename.replace('/', '\\')


def ask_for_plan():
    root = open_dialog_and_gain_focus()
    FILE_DIALOG_OPTIONS = {'filetypes': [('PDDL plan files', '*.pddl'), ('All files', '*.*')],
                           'title': 'Choose PDDL result file'}
    filename = tkFileDialog.askopenfilename(
        **FILE_DIALOG_OPTIONS)  # show an "Open" dialog box and return the path to the selected file
    destroy_root_view(root)
    return filename.replace('/', '\\')


def ask_to_save():
    root = open_dialog_and_gain_focus()
    filename = tkFileDialog.asksaveasfile(mode='w',
                                          filetypes=[('PDDL plan files', '*.pddl'), ('All files', '*.*')],
                                          defaultextension='pddl',
                                          title='Save PDDL file as')
    destroy_root_view(root)
    return filename


def is_file_chosen(file):
    return not file == ''


def check_model_file(file):
    return file[-5:] == '.inpx'


def get_absolute_path_for_file(file):
    try:
        open_file = open(file)
        open_file.close()
    except IOError:
        file = os.path.join(os.path.dirname(folderpath), file)
    return file
