# (c) 2014-2016 Jeremy Wright Apache 2.0 License
import sys

def show(cqObject, rgba=(204, 204, 204, 0.0)):
    import FreeCAD
    from random import random
    import os, tempfile
    try:
        from . import Shared
    except:
        import Shared

    #Convert our rgba values
    r = rgba[0] / 255.0
    g = rgba[1] / 255.0
    b = rgba[2] / 255.0
    a = int(rgba[3] * 100.0)

    # Grab our code editor so we can interact with it
    cqCodePane = Shared.getActiveCodePane()

    if cqCodePane != None:
        # Save our code to a tempfile and render it
        tempFile = tempfile.NamedTemporaryFile(delete=False)
        tempFile.write(cqCodePane.toPlainText().encode('utf-8'))
        tempFile.close()

        docname = os.path.splitext(os.path.basename(cqCodePane.get_path()))[0]

        # Make sure we replace any troublesome characters
        for ch in ['&', '#', '.', '$', '%', ',', ' ']:
            if ch in docname:
                docname = docname.replace(ch, "")

        # Translate dashes so that they can be safetly used since theyare common
        if '-' in docname:
            docname = docname.replace('-', "__")

        # If the matching 3D view has been closed, we need to open a new one
        try:
            FreeCAD.getDocument(docname)
        except NameError:
            # FreeCAD.Console.PrintError("Could not find the model document or invalid characters were used in the filename.\r\n")

            FreeCAD.newDocument(docname)

    ad = FreeCAD.activeDocument()

    if ad == None:
        FreeCAD.newDocument("untitled" + str(random()))
        ad = FreeCAD.activeDocument()

    # If we've got a blank shape name, we have to create a random ID
    if not cqObject.val().label:
        #Generate a random name for this shape in case we are doing multiple shapes
        newName = "Shape" + str(random())
    else:
        # We're going to trust the user to keep labels unique between shapes
        newName = cqObject.val().label

    #Set up the feature in the tree so we can manipulate its properties
    newFeature = ad.addObject("Part::Feature", newName)

    #Change our shape's properties accordingly
    newFeature.ViewObject.ShapeColor = (r, g, b)
    newFeature.ViewObject.Transparency = a
    newFeature.Shape = cqObject.toFreecad()

    ad.recompute()
