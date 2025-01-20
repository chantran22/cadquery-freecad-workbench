# This is a CadQuery script template
# Add your script code below
import cadquery as cq

r = cq.Workplane("front").circle(2.0).extrude(0.15) 
                                       
                                       
show_object(r)
