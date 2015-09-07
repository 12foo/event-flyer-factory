from flask import Flask, render_template, request, json, send_file, after_this_request
from os import path, remove
import requests, tempfile, pdf_builder


app = Flask(__name__)

download_ids = {}

# Proxies event searches (no CORS on the event search).
@app.route("/events/<zipcode>/<radius>")
def find_events(zipcode, radius):
    url = "https://go.berniesanders.com/page/event/search_results?orderby=zip_radius&zip_radius[0]=" +\
        zipcode + "&zip_radius[1]=" + radius + "&country=US&radius_unit=mi&format=json"
    events = requests.get(url)
    return events.text
        
# This builds a PDF and returns a download ID when it is complete.
@app.route("/build", methods=["POST"])
def build_flyer():
    event_pdf = tempfile.NamedTemporaryFile(delete=False)
    pdf_builder.build_pdf(request.json["events"], event_pdf.name)

    # TODO: complete PDF should be a PDF flyer template with the
    # event_pdf stamped onto it. Use pypdf2 for this.
    complete_pdf = event_pdf
    complete_pdf.close()

    download_ids[path.basename(complete_pdf.name)] = complete_pdf.name
    return json.jsonify(download=path.basename(complete_pdf.name))

# Downloads a PDF by ID.
@app.route("/download/<fid>")
def download_flyer(fid):
    if fid not in download_ids:
        return "That download doesn't exist.", 400
    pdf = download_ids[fid]
    del download_ids[fid]

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
