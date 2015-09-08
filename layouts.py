from reportlab.platypus import (Flowable, Spacer, BaseDocTemplate)
from reportlab.platypus.frames import (Frame)
from reportlab.platypus.doctemplate import (PageTemplate)
from reportlab.lib.units import inch

from itertools import chain, repeat

# register fonts for PDFs
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Lato", "fonts/Lato2OFL/Lato-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lato Bold", "fonts/Lato2OFL/Lato-Bold.ttf"))


# A normal-sized event that fits into a 2-column layout.
class Event(Flowable):
    def __init__(self, event):
        Flowable.__init__(self)
        self.event = event
        self.height = 0.7*inch

    def draw(self):
        c = self.canv
        t = c.beginText()
        t.setFont("Lato Bold", 10)
        t.textLine(self.event["name"])
        t.setFont("Lato", 10)
        t.textLine("%s %s" % (self.event["start_dt"], self.event["start_time"]))
        t.textLine(self.event["venue_addr1"])
        c.drawText(t)

# A large event.
class LargeEvent(Flowable):
    def __init__(self, event):
        Flowable.__init__(self)
        self.event = event
        self.height = inch

    def draw(self):
        c = self.canv
        t = c.beginText()
        t.textLine(self.event["name"])
        t.textLine("%s %s" % (self.event["date"], self.event["time"]))
        t.textLine(self.event["venue_addr1"])
        c.drawText(t)

def layout_twocolumn(fname, pagesize, events):
    topspace = 3*inch
    doc = BaseDocTemplate(fname, pagesize=pagesize, leftMargin=6, bottomMargin=6, rightMargin=6, topMargin=6)
    left_column = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-topspace, id="left")
    right_column = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height-topspace, id="right")
    doc.addPageTemplates(PageTemplate(frames=[left_column, right_column]))

    story = []
    for e in events:
        story.append(Event(e))
    doc.build(story)

