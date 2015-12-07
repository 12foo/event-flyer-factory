from lxml import html
import requests, time, colorsys, random

eventsearch_url = 'https://go.berniesanders.com/page/event/search_simple'

event_ids = None
last_sync = None
sync_interval = 2 * 60 * 60

def random_colors(n):
    colors = []
    for i in range(0, n):
        h = i * (360 / n) / 360
        l = random.randint(25, 40) / 100
        s = random.randint(50, 99) / 100
        rgb = tuple(map(lambda n: round(255 * n), colorsys.hls_to_rgb(h, l, s)))
        colors.append('#%02x%02x%02x' % rgb)
    return colors

def get_event_ids():
    global event_ids, last_sync, sync_interval
    if (event_ids is None or int(time.time()) - last_sync > sync_interval):
        page = requests.get(eventsearch_url)
        doc = html.fromstring(page.content)
        options = ((e.text, e.attrib['value']) for e in doc.xpath('//div[@id="advancedform"]//select[@name="event_type[]"]//option[@value!=""]'))
        events = [e for e in options if 'TEST' not in e[0]]
        events = [{'name': e[0][0], 'value': int(e[0][1]), 'color': e[1]} for e in zip(events, random_colors(len(events)))]
        event_ids = events
        last_sync = int(time.time())
    return event_ids

if __name__ == '__main__':
    print(repr(get_event_ids()))
