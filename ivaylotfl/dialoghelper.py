from Tkinter import Tk  # gui library
import tkFileDialog  # file dialog library
from tkMessageBox import showerror
import os.path

folderpath = ''


def show_error_box_with_message(message):
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    showerror('Error',message)


# initializes a file chooser to load the desired model
def ask_for_model():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

    FILE_DIALOG_OPTIONS = {'filetypes': [('PTV Vissim network files', '*.inpx'), ('All files', '*.*')],
                           'title': 'Choose VISSIM model'}

    filename = tkFileDialog.askopenfilename(
        **FILE_DIALOG_OPTIONS)  # show an "Open" dialog box and return the path to the selected file
    global folderpath
    folderpath = filename
    return filename.replace('/', '\\')


def ask_for_plan():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

    FILE_DIALOG_OPTIONS = {'filetypes': [('PDDL plan files', '*.pddl'), ('All files', '*.*')],
                           'title': 'Choose PDDL result file'}

    filename = tkFileDialog.askopenfilename(
        **FILE_DIALOG_OPTIONS)  # show an "Open" dialog box and return the path to the selected file
    return filename.replace('/', '\\')


def ask_to_save():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = tkFileDialog.asksaveasfile(mode='w',
                                          filetypes=[('PDDL plan files', '*.pddl'), ('All files', '*.*')],
                                          defaultextension='pddl',
                                          title='Save PDDL file as')
    return filename


def is_file_chosen(file):
    return not file == ''


def check_model_file(file):
    return file[-5:] == ".inpx"


def get_absolute_path_for_file(file):
    try:
        open_file = open(file)
        open_file.close()
    except IOError:
        file = os.path.join(os.path.dirname(folderpath), file)
    return file
