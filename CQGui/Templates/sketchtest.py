# This is a CadQuery script template
# Add your script code below
import cadquery as cq
from cadquery.vis import show

sketch  = (cq.Sketch()
           .rect(1.0, 4.0)
           .circle(1.0)
           .clean()
           )

res = (cq.Workplane("front")
           .placeSketch(sketch.copy().wires().offset(0.25))
           .extrude(0.5)
        )


#show_object(res, options={"rgba":(204, 204, 204, 0.0)})
show(res)
