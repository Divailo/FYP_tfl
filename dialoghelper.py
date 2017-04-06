from Tkinter import Tk  # gui library
import tkFileDialog  # file dialog library
import os.path

folderpath = ''

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