from flask import Flask, render_template, request, json, send_file, after_this_request
from os import path, remove
import requests, tempfile, os
import pdf_builder, layouts, templates

app = Flask(__name__)

tmpdir = tempfile.mkdtemp(prefix="flyers")

# Proxies event searches (no CORS on the event search).
@app.route("/events")
def find_events():
    url = "https://go.berniesanders.com/page/event/search_results?" + request.query_string.decode("utf-8")
    events = requests.get(url)
    return events.text, events.status_code
        
# Gets a listing of available templates and layouts.
@app.route("/available")
def available():
    event_types = {
        22: { "name": "Registering Voters", "color": "#f55b5b" },
        24: { "name": "Volunteer Activity", "color": "#4acc66" },
        25: { "name": "Volunteer Meeting", "color": "#2d9f46" },
        26: { "name": "Debate Watch Party", "color": "#147fd7" }
    }
    return json.jsonify(templates=templates.templates_dict(), event_types=event_types)

# Gets a preview image of a template/layout combination.
@app.route("/preview/<template>/preview.jpg", defaults={ "layout": None })
@app.route("/preview/<template>/<layout>/preview.jpg")
def generate_preview(template, layout):
    if template not in templates.templates():
        return "Specified template does not exist.", 400
    if layout is None:
        layout = templates.templates()[template].layouts[0].__name__
    if layout not in layouts.layouts():
        return "Specified layout does not exist.", 400
    return send_file(pdf_builder.get_preview(template, layout), mimetype="image/jpeg")

# This builds a PDF and returns a download ID when it is complete.
@app.route("/build", methods=["POST"])
def build_flyer():
    if "layout" not in request.json or "template" not in request.json or "events" not in request.json:
        return "You have to specify template, a layout and a list of events.", 400
    template = request.json["template"]
    if template not in templates.templates():
        return "Specified template does not exist.", 400
    layout = request.json["layout"]
    if layout not in layouts.layouts():
        return "Specified layout does not exist.", 400
    with tempfile.NamedTemporaryFile(dir=tmpdir, delete=False) as event_pdf:
        pdf_builder.build_pdf(template, layout, request.json["events"], event_pdf.name)
        return json.jsonify(download=path.basename(event_pdf.name))

# Downloads a PDF by ID.
@app.route("/download/<fid>")
def download_flyer(fid):
    pdf = os.path.join(tmpdir, fid)

    @after_this_request
    def cleanup(response):
        remove(pdf)
        return response

    return send_file(pdf, as_attachment=True, attachment_filename="flyer.pdf", mimetype="application/pdf")

# Display index page.
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
