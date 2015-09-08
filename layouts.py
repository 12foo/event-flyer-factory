from reportlab.platypus import Flowable, Spacer, BaseDocTemplate, Table, TableStyle, FrameBreak
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
        "small": ParagraphStyle("small", fontName="Lato", fontSize=8, allowWidows=1, splitLongWords=1,
            leading=8),
        "space-after": ParagraphStyle("default", fontName="Lato", fontSize=10, allowWidows=1, splitLongWords=1,
            spaceAfter=0.15*inch),
        "event-title": ParagraphStyle("event-title", fontName="Lato Bold", fontSize=10,
            allowWidows=1, splitLongWords=1),
        "event-time": ParagraphStyle("event-time", fontName="Lato Italic", fontSize=8,
            allowWidows=1, splitLongWords=1, leading=8),
        "event-description": ParagraphStyle("event-description", fontName="Lato Italic", fontSize=7,
            allowWidows=1, splitLongWords=1, spaceAfter=0.2*inch, leading=7),
        "xl-event-title": ParagraphStyle("xl-event-title", fontName="Lato Bold", fontSize=12,
            allowWidows=1, splitLongWords=1, alignment=TA_CENTER, spaceAfter=0.10*inch),
        "xl-event-venue": ParagraphStyle("xl-event-venue", fontName="Lato Bold", fontSize=8,
            allowWidows=1, splitLongWords=1, alignment=TA_CENTER),
        "xl-event-venue-address": ParagraphStyle("xl-event-venue-address", fontName="Lato", fontSize=7,
            allowWidows=1, splitLongWords=1, alignment=TA_CENTER),
        "xl-event-description": ParagraphStyle("xl-event-description", fontName="Lato", fontSize=9,
            allowWidows=1, splitLongWords=1, alignment=TA_CENTER),
        "xs-event-title": ParagraphStyle("xs-event-title", fontName="Lato Bold", fontSize=6,
            allowWidows=1, splitLongWords=1, spaceAfter=0, leading=6),
        "xs-event": ParagraphStyle("xs-event", fontName="Lato", fontSize=6, leading=6,
            allowWidows=1, splitLongWords=1),
        }

# A normal-sized event that fits into a 2-column layout.
class Event:
    def __init__(self, event):
        self.event = event
        self.name = event["name"]
        self.time = "%s %s" % (arrow.get(event["start_dt"], "YYYY-MM-DD HH:mm:ss").format("MM/D/YYYY, h:mma"),
                event["timezone"])
        self.description = html.unescape(event["description"])

        if "venue_addr1" in event and "venue_city" in event:
            addr = event["venue_addr1"].strip()
            city = event["venue_city"].strip()
            if len(addr) > 0 and len(city) > 0:
                self.place = "%s, %s" % (addr, city)
            else:
                self.place = ""
        else:
            self.place = ""

        self.venue_name = self.event["venue_name"]

        try:
            self.first_sentence = re.match(r'(?:[^.:;]+[.:;]){1}', self.description).group()
        except AttributeError:
            self.first_sentence = ""

    def render(self):
        return KeepTogether([
            Paragraph(self.name, styles["event-title"]),
            Spacer(height=3, width=0),
            Paragraph(self.time, styles["event-time"]),
            Paragraph(self.venue_name, styles["small"]),
            Paragraph(self.place, styles["small"]),
            Spacer(height=3, width=0),
            Paragraph(self.first_sentence, styles["event-description"]),
            ])

# A tiny event
class XSEvent(Event):
    table_style = TableStyle([("FONT", (0, 0), (0, -1), "FontAwesome"),
                              ("ALIGNMENT", (0, 0), (0, -1), "CENTER"),
                              ("VALIGN", (0, 0), (-1, -1), "TOP"),
                              ("SIZE", (0, 0), (-1, -1), 6),
                              ("LEFTPADDING", (0, 0), (-1, -1), 3),
                              ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                              ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
                              ("BOTTOMPADDING", (0, 1), (-1, 1), 0),
                              ("LEADING", (0, 0), (-1, -1), 6),
                              ])

    def __init__(self, event):
        Event.__init__(self, event)

    def render(self):
        venue = [["\uf017", Paragraph(self.time, styles["xs-event"])],
                 ["\uf041", Paragraph(self.venue_name, styles["xs-event"])],
                 ["", Paragraph(self.place, styles["xs-event"])]]
        table = Table(venue, style=self.table_style, spaceAfter=8, colWidths=[8, None])
        table.hAlign = "LEFT"
        table.vAlign = "TOP"
        return KeepTogether([
            Paragraph(self.name, styles["xs-event-title"]),
            table,
            ])

# An extra-large event
class XLEvent(Event):
    def __init__(self, event):
        Event.__init__(self, event)

    def render(self):
        e = []
        e.append(Paragraph(self.name, styles["xl-event-title"]))
        e.append(Paragraph("%s, <b>%s</b>" % (self.time, self.venue_name), styles["xl-event-venue"]))
        if len(self.place) > 0:
            e.append(Paragraph(self.place, styles["xl-event-venue-address"]))
        e.append(Paragraph(self.description, styles["xl-event-description"]))
        return KeepTogether(e)


# Spacing line with a star
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
    name = "Two Columns (~10 events)"
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
    name = "Large Events (3-4 events)"
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


class ThreeColumnLayout(Layout):
    name = "Three Columns, extra-tiny events (~20-30 events)"
    description = "A three-column layout with extra-tiny events. Useful if you need to pack a lot of them " +\
        "into one flyer."
        
    def fill(self, fname, pagesize, events, topspace=3*inch, bottomspace=0):
        doc = BaseDocTemplate(fname, pagesize=pagesize, leftMargin=6, bottomMargin=6, rightMargin=6, topMargin=6)
        left_column = Frame(doc.leftMargin, doc.bottomMargin, doc.width/3-6, doc.height-topspace, id="left")
        middle_column = Frame(doc.leftMargin+doc.width/3+6, doc.bottomMargin, doc.width/3-6, doc.height-topspace, id="middle")
        right_column = Frame(doc.leftMargin+2*doc.width/3+6, doc.bottomMargin, doc.width/3-6, doc.height-topspace, id="right")
        doc.addPageTemplates(PageTemplate(frames=[left_column, middle_column, right_column]))

        story = []
        for e in events:
            story.append(XSEvent(e).render())
        doc.build(story)

class FeaturedLayout(Layout):
    name = "Featured Event + 2 columns (~7 events)"
    description = "One large main event, and 2 columns with further events."
        
    def fill(self, fname, pagesize, events, topspace=3*inch, bottomspace=0):
        doc = BaseDocTemplate(fname, pagesize=pagesize, leftMargin=6, bottomMargin=6, rightMargin=6, topMargin=topspace)
        featured = Frame(doc.leftMargin+0.4*inch, doc.bottomMargin+3*doc.height/4, doc.width-6-0.8*inch,
                doc.height/3, id="featured")
        left_column = Frame(doc.leftMargin, doc.bottomMargin, doc.width/2-6, 3*doc.height/4, id="left")
        right_column = Frame(doc.leftMargin+doc.width/2+6, doc.bottomMargin, doc.width/2-6, 3*doc.height/4, id="right")
        doc.addPageTemplates(PageTemplate(frames=[featured, left_column, right_column]))

        story = []
        story.append(XLEvent(events[0]).render())
        story.append(SpacerLine(3*inch, 0))
        story.append(FrameBreak())
        for e in events[1:]:
            story.append(Event(e).render())
        doc.build(story)

layouts = {c.__name__: c for c in Layout.__subclasses__()}
