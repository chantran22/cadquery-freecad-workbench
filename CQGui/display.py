# Define the show_object function which CadQuery execution environments need to provide
def show_object(cq_object, options=None):
    import cadquery as cq
    import Part, FreeCAD, FreeCADGui
    from PySide import QtGui
    import tempfile
    import os

    # Temporary file for exporting STEP data
    temp_file = tempfile.NamedTemporaryFile(suffix=".step", delete=False)
    temp_file.close()  # Close the file to allow CadQuery to write to it

    # Keep track of the feature name
    feature_name = None

    # Check to see what type of object we are dealing with
    try:
        if isinstance(cq_object, cq.Workplane):
            # Handle the label if the user set it
            if cq_object.val().label:
                feature_name = cq_object.val().label

            # Export the object as a STEP file
            cq_object.val().export(temp_file.name)
        elif isinstance(cq_object, cq.Shape):
            # If we have a solid, we can export it directly
            cq_object.export(temp_file.name)
        elif hasattr(cq_object, "wrapped"):
            # Handle the label if the user has it set
            if hasattr(cq_object, "label"):
                feature_name = cq_object.label

            from build123d import export_step
            export_step(cq_object, temp_file.name)
        elif hasattr(cq_object, "_obj"):
            # Handle the label if the user has it set
            if hasattr(cq_object, "label"):
                feature_name = cq_object.label

            from build123d import export_step
            export_step(cq_object._obj, temp_file.name)
        else:
            print("Object type not supported for display: ", type(cq_object).__name__)
            return
    except Exception as e:
        print("Error exporting STEP file:", e)
        return

    # Get the title of the current document so that we can create/find the FreeCAD part window
    doc_name = "untitled"
    mw = FreeCADGui.getMainWindow()
    mdi_area = mw.findChild(QtGui.QMdiArea)
    active_subwindow = mdi_area.activeSubWindow()
    if active_subwindow:
        doc_name = active_subwindow.windowTitle().split(" :")[0]
        doc_name = doc_name.split(".py")[0]

    # Create or find the document that corresponds to this code pane
    try:
        FreeCAD.getDocument(doc_name)
    except NameError:
        FreeCAD.newDocument(doc_name)
    ad = FreeCAD.activeDocument()

    # Import the STEP file into FreeCAD
    try:
        part_shape = Part.Shape()
        part_shape.read(temp_file.name)  # Use Part.Shape.read() to load the STEP file
    except Exception as e:
        print("Error importing STEP file into FreeCAD:", e)
        return
    finally:
        # Clean up the temporary file
        os.remove(temp_file.name)

    # If the user wanted to use a specific name in the tree, use it
    if not feature_name:
        feature_name = doc_name

    # Find the feature in the document, if it exists
    cur_feature = None
    for feat in ad.Objects:
        if feat.Name == feature_name or feat.Label == feature_name:
            cur_feature = feat
            break

    # Decide whether to create a new object or update an existing one
    if cur_feature:
        # Update the existing object
        cur_feature = ad.getObject(feature_name)
        cur_feature.Shape = part_shape
    else:
        cur_feature = ad.addObject("Part::Feature", feature_name)
        cur_feature.Label = feature_name
        cur_feature.Shape = part_shape

    # Apply any options to the imported shape
    if options:
        # Handle a transparency change, if requested
        if "alpha" in options:
            # Make sure that the alpha is scaled between 0 and 255
            alpha = int(options["alpha"] * 100)
            cur_feature.ViewObject.Transparency = alpha

        # Handle a color change, if requested
        if "color" in options:
            cur_feature.ViewObject.ShapeColor = options["color"]

    # Make sure the document updates
    ad.recompute()
