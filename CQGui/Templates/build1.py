# This is a CadQuery script template
# Add your script code below
from build123d import *


k=1000**(-3)

length, width, thickness = 80.0, 60.0, 10.0
bp = Box(length, width, thickness)


show_object(bp)
