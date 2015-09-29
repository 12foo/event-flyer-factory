import layouts

class Template(object):
    pdf = None
    name = None
    description = None
    creator = None
    link = None
    layouts = []

class BerniePartyTwoUp(Template):
    name = "Bernie Party 2-up"
    description = "Go Bernie Go! A 2-up debate watching invite."
    creator = "Gavin MacPherson"
    layouts = [layouts.BerniePartyTwoUp]


cached_templates = None
def templates():
    global cached_templates
    if cached_templates is None:
        cached_templates = {c.__name__: c for c in Template.__subclasses__()}
    return cached_templates

cached_templates_dict = None
def templates_dict():
    global cached_templates_dict
    if cached_templates_dict is None:
        ts = []
        for t in Template.__subclasses__():
            ls = []
            for l in t.layouts:
                ls.append({ "id": l.__name__, "name": l.name, "description": l.description, "events": l.events })
            ts.append({ "id": t.__name__, "name": t.name, "description": t.description, "creator": t.creator,
                "link": t.link, "layouts": ls })
        cached_templates_dict = ts
    return cached_templates_dict
