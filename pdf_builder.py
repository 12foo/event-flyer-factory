from reportlab.lib.units import inch

import layouts

def build_pdf(events, fname):
    layouts.layout_twocolumn(fname, (5*inch, 11*inch), events)
