# Bernie 2016 Event Flyer Factory

This is a little web-based tool that turns selected events from Bernie's 
campaign page into PDF flyers. Right now, this is basically just a
proof of concept-- it searches events and builds the PDF, but it's not
very flyer-like yet.

## Requirements

This tool requires Python 3 (may run under Python 2). The frontend is
written in [mithril.js](https://lhorie.github.io/mithril/) and CoffeeScript.
To compile the frontend, node.js and NPM must be installed also.

## How to run

```bash
git clone https://github.com/12foo/event-flyer-factory
cd event-flyer-factory
git submodule update
# (activate your virtualenv if you have one)
pip install -r requirements.txt
# you need to install lxml separately for deployment reasons
pip install lxml
npm install
npm run build 
# (for development, use npm run dev to automatically recompile js/css on changes)
python server.py
```

Then, open http://localhost:5000 in your browser.

## Contributing

Many features are still missing! Check the issues page for some pointers.
