from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer)

# An event PDF object that can be flowed onto a PDF page.
class Event(Flowable):
    def __init__(self, name, time, date, timezone, venue_name, venue_address):
        Flowable.__init__(self)
        self.height = inch
        self.name = name
        self.time = time
        self.date = date
        self.timezone = timezone
        self.venue_name = venue_name
        self.venue_address = venue_address

    def __repr__(self):
        return "Event(name=%s)" % self.name

    def draw(self):
        c = self.canv
        t = c.beginText()
        t.textLine(self.name)
        t.textLine("%s %s" % (self.date, self.time))
        t.textLine(self.venue_address)
        c.drawText(t)

def build_pdf(events, fname):
    pdf = SimpleDocTemplate(fname, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    story.append(Spacer(0, 5*inch))

    for e in events:
        flow_event = Event(e["name"], e["start_time"], e["start_dt"], e["timezone"], e["venue_name"], e["venue_addr1"])
        story.append(flow_event)

    pdf.build(story)
