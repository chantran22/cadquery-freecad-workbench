# (c) 2014-2025 CadQuery Developers

"""
CadQuery GUI init module for FreeCAD
This adds a workbench with a scripting editor to FreeCAD's GUI.
"""

import os
import Part
import FreeCAD
import FreeCADGui
from cadquery import cq
#from CQGui import myfunc

from CQGui.Command import (
    CadQueryHelp,
    CadQueryNewScript,
    CadQueryOpenScript,
    CadQuerySaveScript,
    CadQuerySaveAsScript,
    CadQueryExecuteScript,
    CadQueryToggleCommentScript,
    CadQueryValidateScript,
    CadQueryClearOutput,
    
)


class CadQueryWorkbench(Workbench):
    """CadQuery workbench for FreeCAD"""

    MenuText = "CadQuery"
    ToolTip = "CadQuery workbench"
    script_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
    Icon = os.path.join(script_dir, "CQGui", "icons", "CQ_Logo.svg")
    #Icon = os.path.join(os.path.dirname(__file__), "CQGui", "icons", "CQ_Logo.svg")

    closedWidgets = []  # Keeps track of which workbenches we have hidden so we can reshow them

    def Initialize(self):
        """Initialize the CadQuery workbench"""
        self.appendMenu("CadQuery", ["CadQueryNewScript", "CadQueryOpenScript" ,"CadQuerySaveScript", "CadQuerySaveAsScript", "CadQueryExecuteScript"])
        self.appendMenu("CadQuery", [ "CadQueryToggleCommentScript", "CadQueryValidateScript",  "CadQueryClearOutput", "CadQueryHelp"])

    def Activated(self):
        """Actions to perform when the CadQuery workbench is activated"""
        import cadquery
        from PySide import QtGui

        msg = QtGui.QApplication.translate(
            "cqCodeWidget",
            f"CadQuery {cadquery.__version__}\r\n"
            "CadQuery is a parametric scripting API for creating and traversing CAD models\r\n"
            "Author: David Cowden\r\n"
            "License: Apache-2.0\r\n"
            "Website: https://github.com/dcowden/cadquery
            Website: https://github.com/gumyr/build123d\r\n",
            None,
        )
        FreeCAD.Console.PrintMessage(msg)

        # Getting the main window to ensure the report view is visible
        mw = FreeCADGui.getMainWindow()
        dockWidgets = mw.findChildren(QtGui.QDockWidget)

        for widget in dockWidgets:
            if widget.objectName() == "Report view":
                widget.setVisible(True)

    def AutoExecute(self):
        """Automatically execute a script when a file is reloaded"""
        try:
            from CQGui import Command
            Command.CadQueryExecuteScript().Activated()
        except Exception as e:
            FreeCAD.Console.PrintError(f"Error in AutoExecute: {e}\r\n")

    def Deactivated(self):
        """Actions to perform when the CadQuery workbench is deactivated"""
        pass




FreeCADGui.addCommand('CadQueryOpenScript', CadQueryOpenScript())
FreeCADGui.addCommand('CadQuerySaveScript', CadQuerySaveScript())
FreeCADGui.addCommand('CadQuerySaveAsScript', CadQuerySaveAsScript())
FreeCADGui.addCommand('CadQueryExecuteScript', CadQueryExecuteScript())
FreeCADGui.addCommand('CadQueryNewScript', CadQueryNewScript())

FreeCADGui.addCommand('CadQueryValidateScript', CadQueryValidateScript())
FreeCADGui.addCommand('CadQueryToggleCommentScript', CadQueryToggleCommentScript())

FreeCADGui.addCommand('CadQueryClearOutput', CadQueryClearOutput())
FreeCADGui.addCommand('CadQueryHelp', CadQueryHelp())

FreeCADGui.addWorkbench(CadQueryWorkbench())

