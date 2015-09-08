from reportlab.lib.units import inch

import layouts

def build_pdf(layout_name, events, fname):
    layout = layouts.layouts[layout_name]
    layout.fill(layout, fname, (5*inch, 11*inch), events)
