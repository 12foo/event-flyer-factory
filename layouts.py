from reportlab.platypus import (Flowable, Spacer, BaseDocTemplate)
from reportlab.platypus.frames import Frame
from reportlab.platypus.flowables import KeepTogether
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch

from itertools import chain, repeat
import arrow, html, re

# register fonts for PDFs
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("FontAwesome", "fonts/fontawesome-webfont.ttf"))
pdfmetrics.registerFont(TTFont("Lato", "fonts/Lato2OFL/Lato-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Lato Bold", "fonts/Lato2OFL/Lato-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Lato Italic", "fonts/Lato2OFL/Lato-Italic.ttf"))

dummy_event = {
        "name": "Placeholder Event for Flyer Factory",
        "start_dt": "2015-09-08 12:00:00",
        "timezone": "PDT",
        "description": "Fremont for Bernie Sanders is hosting Mario Brown of the&nbsp;Washington State Democratic Chairs Organization to learn more about caucusing for Bernie Sanders in 2016.&nbsp; Mario will explain how the caucus works in Washington and how we can get involved to get Senator Sanders elected in November!  ...",
        "venue_addr1": "1234 Somestreet NW",
        "venue_city": "Seattle",
        "venue_name": "A venue somewhere",
        "venue_zip": "98109"
        }

styles = {
        "default": ParagraphStyle("default", fontName="Lato", fontSize=10, allowWidows=1, splitLongWords=1),
        "space-after": ParagraphStyle("default", fontName="Lato", fontSize=10, allowWidows=1, splitLongWords=1,
            spaceAfter=0.15*inch),
        "event-title": ParagraphStyle("event-title", fontName="Lato Bold", fontSize=10, allowWidows=1, splitLongWords=1),
        "event-time": ParagraphStyle("event-time", fontName="Lato Italic", fontSize=10, allowWidows=1, splitLongWords=1),
        "xl-event-title": ParagraphStyle("xl-event-title", fontName="Lato Bold", fontSize=12, allowWidows=1, splitLongWords=1, alignment=TA_CENTER, spaceAfter=0.10*inch),
        "xl-event-time": ParagraphStyle("event-time", fontName="Lato Italic", fontSize=10, allowWidows=1, splitLongWords=1, alignment=TA_CENTER, spaceAfter=0.10*inch),
        "xl-event-description": ParagraphStyle("xl-event-description", fontName="Lato", fontSize=9, allowWidows=1, splitLongWords=1, alignment=TA_CENTER)
        }

# A normal-sized event that fits into a 2-column layout.
class Event:
    def __init__(self, event):
        Flowable.__init__(self)
        self.event = event
        self.name = event["name"]
        self.time = "%s %s" % (arrow.get(event["start_dt"], "YYYY-MM-DD HH:mm:ss").format("MM/D/YYYY, h:mma"),
                event["timezone"])
        self.description = html.unescape(event["description"])
        self.first_sentence = re.match(r'(?:[^.:;]+[.:;]){1}', self.description).group()
        self.height = 0.7*inch

    def render(self):
        return KeepTogether([
            Paragraph(self.name, styles["event-title"]),
            Paragraph(self.time, styles["event-time"]),
            Paragraph(self.event["venue_addr1"], styles["space-after"]),
            ])


# An extra-large event
class XLEvent(Event):
    def __init__(self, event):
        Event.__init__(self, event)
        self.height = inch

    def render(self):
        return KeepTogether([
            Paragraph(self.name, styles["xl-event-title"]),
            Paragraph(self.time, styles["xl-event-time"]),
            Paragraph(self.description, styles["xl-event-description"]),
            ])


class SpacerLine(Flowable):
    def __init__(self, width, margin):
        Flowable.__init__(self)
        self.width = width
        self.margin = margin
        self.hAlign = "CENTER"
        self.height = 0.5*inch
 
    def draw(self):
        self.canv.saveState()
        self.canv.setLineWidth(0.25)
        self.canv.line(0, self.height/2, self.width/2-15, self.height/2)
        self.canv.setFont("FontAwesome", 11)
        self.canv.drawCentredString(self.width/2, self.height/2-4, "\uf005")
        self.canv.line(self.width/2+15, self.height/2, self.width, self.height/2)
        self.canv.restoreState()


# Base layout (do not make available to frontend)        
class Layout:
    name = "Layout"
    description = ""

    def fill(self, fname, pagesize, events, topspace=0, bottomspace=0):
        doc = BaseDocTemplate(fname, pagesize=pagesize, leftMargin=6, bottomMargin=6, rightMargin=6, topMargin=6)
        doc.build([])



class TwoColumnLayout(Layout):
    name = "Two Columns"
    description = "A simple two-column layout. This is a good fit if you have around 10 events."
        
    def fill(self, fname, pagesize, events, topspace=3*inch, bottomspace=0):
        doc = BaseDocTemplate(fname, pagesize=pagesize, leftMargin=6, bottomMargin=6, rightMargin=6, topMargin=6)
        left_column = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, doc.height-topspace, id="left")
        right_column = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, doc.height-topspace, id="right")
        doc.addPageTemplates(PageTemplate(frames=[left_column, right_column]))

        story = []
        for e in events:
            story.append(Event(e).render())
        doc.build(story)


class LargeLayout(Layout):
    name = "Large Events"
    description = "A layout that presents a small number of events large and in detail. (3-4 events)"
        
    def fill(self, fname, pagesize, events, topspace=3*inch, bottomspace=0):
        doc = BaseDocTemplate(fname, pagesize=pagesize, leftMargin=0.5*inch, bottomMargin=6, rightMargin=0.5*inch, topMargin=6)
        column = Frame(doc.leftMargin, doc.bottomMargin, doc.width-6, doc.height-topspace, id="large")
        doc.addPageTemplates(PageTemplate(frames=[column]))

        story = []
        for e in events:
            story.append(XLEvent(e).render())
            story.append(SpacerLine(3*inch, 0))
        story = story[:-1]
        doc.build(story)

layouts = {c.__name__: c for c in Layout.__subclasses__()}
