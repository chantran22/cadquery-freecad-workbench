# -*- coding: utf-8 -*-
# (c) 2014-2025 CadQuery Developers

"""Adds all of the commands that are used for the menus of the CadQuery module"""
import os
import sys
import tempfile
import random
import inspect
import cadquery as cq
from CodeEditor import CodeEditor
#from cadquery import Shared
import Shared
#from PySide import QtGui
#import FreeCAD
#import FreeCADGui
from contextlib import contextmanager
import FreeCAD, FreeCADGui
from PySide import QtGui
from CQGui.display import show_object
#from CQGui.ImportCQ import open
#from ExportCQ import save
from CQGui.HelpDialog import HelpDialog

# class CadQueryStableInstall:
    # """
    # Allows the user to easily attempt a manual install of the stable version of CadQuery
    # """

    # def GetResources(self):
        # return {"MenuText": "Install CadQuery Stable",
                # "Accel": "",
                # "ToolTip": "Installs the stable version of CadQuery",
                # "Pixmap": ":/icons/preferences-system.svg"}

    # def IsActive(self):
        # return True

    # def Activated(self):
        # import subprocess
        # print("Starting to install CadQuery stable...")
        # subprocess.run(["python", "-m", "pip", "install", "--upgrade", "cadquery==2.5.2"], capture_output=False)
        # subprocess.run(["python", "-m", "pip", "install", "--upgrade", "cadquery-ocp==7.7.2"], capture_output=False)
        # print("CadQuery stable has been installed! Please restart FreeCAD.")

class ImportCQ:
    @staticmethod
    def open(filename):
        # All of the CQGui.* calls in the Python console break after opening if we don't do this
        FreeCADGui.doCommand("import FreeCADGui as CQGui")

        # Get the script's directory
        script_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))

        # Getting the main window will allow us to find the children we need to work with
        mw = FreeCADGui.getMainWindow()

        # Grab just the file name from the path/file that's being executed
        docname = os.path.basename(filename)

        # Pull the font size from the FreeCAD-stored settings
        fontSize = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/cadquery-freecad-module").GetInt("fontSize")

        # Set up the code editor
        codePane = CodeEditor()
        codePane.setFont(QtGui.QFont('SansSerif', fontSize))
        codePane.setObjectName("cqCodePane_" + os.path.splitext(os.path.basename(filename))[0])

        mdi = mw.findChild(QtGui.QMdiArea)
        # Add a code editor widget to the mdi area
        sub = mdi.addSubWindow(codePane)
        sub.setWindowTitle(docname)
        sub.setWindowIcon(QtGui.QIcon(':/icons/applications-python.svg'))
        sub.show()
        mw.update()

        # Pull the text of the CQ script file into our code pane
        codePane.open(filename)

        msg = QtGui.QApplication.translate(
            "cqCodeWidget",
            "Opened ",
            None)
        FreeCAD.Console.PrintMessage(msg + filename + "\r\n")
    
class CadQueryNewScript:
    """CadQuery's command to start a new script file."""
    def GetResources(self):
        return {"MenuText": "New Script",
                "Accel": "Alt+N",
                "ToolTip": "Starts a new CadQuery script",
                "Pixmap": ":/icons/document-new.svg"}

    def IsActive(self):
        return True

    def Activated(self):
        # Resolve module path using the current file directory
        module_base_path = os.path.dirname(inspect.getfile(inspect.currentframe()))
        templ_dir_path = os.path.join(module_base_path, 'Templates')

        # Use the integrated ImportCQ library to open CQ files
        ImportCQ.open(os.path.join(templ_dir_path, 'script_template.py'))

        FreeCAD.Console.PrintMessage("Please save this template file as another name before creating any others.\r\n")

class CadQueryOpenScript:
    """CadQuery's command to open a script file."""
    previousPath = None

    def GetResources(self):
        return {
            "MenuText": "Open Script",
            "Accel": "Alt+O",
            "ToolTip": "Opens a CadQuery script from disk",
            "Pixmap": ":/icons/document-open.svg"
        }

    def IsActive(self):
        return True

    def Activated(self):
        mw = FreeCADGui.getMainWindow()

        if self.previousPath is None:
            # Resolve the path to the examples directory cadquery\CQGui\Templates
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            exs_dir_path = os.path.join(current_script_dir,  'cadquery', 'CQGui', 'Templates')
            self.previousPath = exs_dir_path

        # Open the file dialog to select a script
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            mw,
            mw.tr("Open CadQuery Script"),
            self.previousPath,
            mw.tr("CadQuery Files (*.py)")
        )

        # Make sure the user didn't click cancel
        if filename:
            self.previousPath = filename
            # Append the script's directory to sys.path
            sys.path.append(os.path.dirname(filename))
            # Open the script using ImportCQ
            ImportCQ.open(filename)


def save(filename=None):
    """
    Allows us to save the CQ script file to disk.
    :param filename: The path and file name to save to. If not provided, we try to pull it from the code pane itself.
    """
    # Grab our code editor so we can interact with it
    cqCodePane = Shared.getActiveCodePane()

    if cqCodePane is None:
        FreeCAD.Console.PrintError("Nothing to save.\r\n")
        return

    # If no filename is provided, use the existing path in the editor
    if filename is None:
        filename = cqCodePane.get_path()

    # Save the file content
    cqCodePane.save(filename)

    # Notify the user
    msg = QtGui.QApplication.translate("cqCodeWidget", "Saved ", None)
    FreeCAD.Console.PrintMessage(msg + os.path.basename(filename) + "\r\n")

class CadQuerySaveScript:
    """CadQuery's command to save a script file"""

    def GetResources(self):
        return {
            "MenuText": "Save Script",
            "Accel": "Alt+S",
            "ToolTip": "Saves the CadQuery script to disk",
            "Pixmap": ":/icons/document-save.svg"
        }

    def IsActive(self):
        return True

    def Activated(self):
        # Grab our code editor so we can interact with it
        cqCodePane = Shared.getActiveCodePane()

        # If there are no windows open, there is nothing to save
        if cqCodePane is None:
            FreeCAD.Console.PrintError("Nothing to save.\r\n")
            return

        # Get the current script path
        current_path = cqCodePane.get_path()

        # Check if the file is a template or example
        if not current_path or os.path.basename(current_path) == 'script_template.py' or \
                os.path.split(current_path)[0].endswith('FreeCAD'):
            FreeCAD.Console.PrintError("You cannot save over a blank file, example file, or template file.\r\n")
            CadQuerySaveAsScript().Activated()
            return

        # Save the file using the provided save function
        save(current_path)

        # Execute the script if the user has enabled this option
        execute_on_save = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/cadquery-freecad-module").GetBool("executeOnSave")
        if execute_on_save:
            CadQueryExecuteScript().Activated()
            


class CadQueryExecuteScript:
    """CadQuery's command to execute a script file"""

    def GetResources(self):
        return {
            "MenuText": "Execute Script",
            "Accel": FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/cadquery-freecad-module").GetString("executeKeybinding"),
            "ToolTip": "Executes the CadQuery script",
            "Pixmap": ":/icons/media-playback-start.svg"
        }

    def IsActive(self):
        return True

    def Activated(self):
        # Grab the code editor to interact with it
        cqCodePane = Shared.getActiveCodePane()

        # Clear the old render before re-rendering
        Shared.clearActiveDocument()

        scriptText = cqCodePane.toPlainText().encode('utf-8')

        # Set environment variables to help the user
        os.environ["MYSCRIPT_FULL_PATH"] = cqCodePane.get_path()
        os.environ["MYSCRIPT_DIR"] = os.path.dirname(os.path.abspath(cqCodePane.get_path()))

        # Save the code to a temporary file
        tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
        tempFile.write(scriptText)
        tempFile.close()

        try:
            # Execute the script
            
            exec_globals = {
              "show_object": show_object,  
              "show": show_object  
             }
            with open(tempFile.name, "r") as f:
                exec(f.read(), exec_globals)

            msg = QtGui.QApplication.translate(
                "cqCodeWidget",
                "Executed ",
                None
            )
            FreeCAD.Console.PrintMessage(msg + cqCodePane.get_path() + "\r\n")

        except Exception as e:
            FreeCAD.Console.PrintError("Error executing script: " + str(e) + "\r\n")
        finally:
            # Clean up the temporary file
            os.remove(tempFile.name)


@contextmanager
def revert_sys_modules():
    """Context manager to temporarily revert changes to sys.modules."""
    import sys
    original_modules = sys.modules.copy()
    try:
        yield
    finally:
        sys.modules.clear()
        sys.modules.update(original_modules)


class CadQueryHelp:
    """Opens a help dialog, allowing the user to access documentation and information about CadQuery"""

    def GetResources(self):
        return {"MenuText": "Help",
                "Accel": "",
                "ToolTip": "Opens the Help dialog",
                "Pixmap": ":/icons/help-browser.svg"}

    def IsActive(self):
        return True

    def Activated(self):
        win = HelpDialog()

        win.exec_()
