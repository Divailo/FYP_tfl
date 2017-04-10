from Tkinter import Tk  # gui library
import tkFileDialog  # file dialog library
from tkMessageBox import showerror
import os.path

folderpath = ''

def create_error_box(message):
    showerror('Error', message)


# initializes a file chooser to load the desired model
def ask_for_model():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

    FILE_DIALOG_OPTIONS = {'filetypes': [('PTV Vissim network files', '*.inpx'), ('All files', '*.*')],
                           'title': 'Choose VISSIM model'}

    filename = tkFileDialog.askopenfilename(**FILE_DIALOG_OPTIONS)  # show an "Open" dialog box and return the path to the selected file
    directory = os.path.split(filename)[0]
    global folderpath
    folderpath = directory.replace('/', '\\')
    # print folderpath
    return filename.replace('/', '\\')


def ask_for_plan():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

    FILE_DIALOG_OPTIONS = {'filetypes': [('PDDL plan files', '*.pddl'), ('All files', '*.*')],
                           'title': 'Choose PDDL result file'}

    filename = tkFileDialog.askopenfilename(**FILE_DIALOG_OPTIONS)  # show an "Open" dialog box and return the path to the selected file
    directory = os.path.split(filename)[0]
    global folderpath
    folderpath = directory.replace('/', '\\')
    # print folderpath
    return filename.replace('/', '\\')


def check_file_chosen(file):
    return not file == ''


def check_model_file(file):
    return file[-5:] == ".inpx"


def _get_absolute_path_for_file(file):
    try:
        open_file = open(file)
        open_file.close()
    except IOError:
        file = folderpath + '\\' + file

    return file