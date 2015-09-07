# Bernie 2016 Event Flyer Factory

This is a little web-based tool that turns selected events from Bernie's 
campaign page into PDF flyers. Right now, this is basically just a
proof of concept-- it searches events and builds the PDF, but it's not
very flyer-like yet.

## Requirements

This tool requires Python 3 (may run under Python 2). The frontend is
written in [mithril.js](https://lhorie.github.io/mithril/) and CoffeeScript.

## How to run

```
git clone [...]
cd bernie-eff
pip install -r requirements.txt
python server.py
```

Then, open http://localhost:5000 in your browser.

## Contributing

Many features are still missing! Check the issues page for some pointers.
