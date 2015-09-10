from reportlab.lib.units import inch

import layouts

def build_pdf(layout_name, events, fname):
    layout = layouts.layouts[layout_name]
    pagesize = (8.5*inch, 11*inch)
    layout.fill(layout, fname, pagesize, events, pagesize[1]/3, 6, 0.5*inch)
