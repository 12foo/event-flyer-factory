// Generated by CoffeeScript 1.10.0
(function() {
  var EventArrange, EventSearch, EventSelect, PDFBuild, Shared, state;

  state = {
    searchZip: m.prop(null),
    searchRadius: m.prop(100),
    searching: m.prop(false),
    building: m.prop(false),
    events: m.prop([]),
    selected: m.prop([])
  };

  Shared = {
    eventBody: function(e) {
      return [m('.event-name', e.name), m('.event-time', e.start_dt), m('.event-venue', e.venue_name)];
    }
  };

  EventSearch = {
    controller: function() {
      return {
        performSearch: function() {
          state.searching(true);
          m.redraw();
          return m.request({
            method: 'GET',
            url: 'events/' + state.searchZip() + '/' + state.searchRadius() + '&country=US&radius_unit=mi&format=json'
          }).then(function(r) {
            state.selected([]);
            state.events(r.results);
            return state.searching(false);
          });
        }
      };
    },
    view: function(c) {
      return m('div.panel.panel-default', [
        m('div.panel-heading', '1. Search for Events'), m('div.panel-body', m('form.form-inline', {
          onsubmit: function(e) {
            e.preventDefault();
            return c.performSearch();
          }
        }, m('.row', [
          m('.col-md-4', [
            m('input[type=text].form-control', {
              placeholder: 'Zip Code',
              onchange: m.withAttr('value', state.searchZip),
              value: state.searchZip()
            })
          ]), m('.col-md-4', [
            m('input[type=text].form-control', {
              placeholder: 'Radius (m)',
              onchange: m.withAttr('value', state.searchRadius),
              value: state.searchRadius()
            })
          ]), m('.col-md-4', [m('button[type=submit].btn.btn-primary', 'Search')])
        ])))
      ]);
    }
  };

  EventSelect = {
    controller: function() {
      return {
        renderEvent: function(e) {
          return m('.event.row', [
            m('.col-xs-10', Shared.eventBody(e)), m('.col-xs-2', m('button.btn.btn-success.btn-xs', {
              onclick: function() {
                return state.selected(_.xor(state.selected(), [e]));
              }
            }, 'Add'))
          ]);
        }
      };
    },
    view: function(c) {
      if (state.searching()) {
        return m('.text-muted.center', 'Searching! Please wait...');
      } else {
        if (state.events().length === 0) {
          return m('.text-muted.center', 'No results. Perform a search above.');
        } else {
          return m('div.panel.panel-default', [m('.panel.panel-heading', '2. Select Events'), m('.panel-body', m('.scrollable', state.events().map(c.renderEvent)))]);
        }
      }
    }
  };

  EventArrange = {
    controller: function() {
      var moveEvent, removeEvent;
      removeEvent = function(e) {
        return state.selected(_.without(state.selected(), e));
      };
      moveEvent = function(e, move) {
        var i, sel;
        sel = state.selected();
        i = _.indexOf(sel, e);
        sel.splice(i, 1);
        i = i + move;
        if (i < 0) {
          i = 0;
        }
        if (i > sel.length) {
          i = sel.length;
        }
        sel.splice(i, 0, e);
        return state.selected(sel);
      };
      return {
        renderEvent: function(e) {
          return m('.event.row', [
            m('.col-xs-10', Shared.eventBody(e)), m('.col-xs-2', m('button.btn.btn-default.btn-xs', {
              onclick: function() {
                return moveEvent(e, -1);
              }
            }, '▲'), m('br'), m('button.btn.btn-danger.btn-xs', {
              onclick: function() {
                return removeEvent(e);
              }
            }, 'X'), m('br'), m('button.btn.btn-default.btn-xs', {
              onclick: function() {
                return moveEvent(e, 1);
              }
            }, '▼'))
          ]);
        }
      };
    },
    view: function(c) {
      if (state.selected().length > 0) {
        return m('.panel.panel-default', [m('.panel.panel-heading', '3. Arrange events'), m('.panel-body', m('.scrollable', state.selected().map(c.renderEvent)))]);
      }
    }
  };

  PDFBuild = {
    controller: function() {
      var isSelected;
      isSelected = function(e) {
        return _.includes(state.selected(), e.id);
      };
      return {
        buildPDF: function() {
          state.building(true);
          m.redraw();
          return m.request({
            method: 'POST',
            url: 'build',
            data: {
              events: state.selected()
            }
          }).then(function(r) {
            state.building(false);
            if (r.download) {
              return window.location.href = 'download/' + r.download;
            } else {

            }
          });
        }
      };
    },
    view: function(c) {
      if (state.selected().length > 0) {
        return m('.panel.panel-default', [
          m('.panel-heading', '4. Layout, Template and Build'), m('.panel-body', [
            m('', state.selected().length + ' events selected.'), m('button.btn.btn-primary', {
              "class": state.building() ? 'disabled' : '',
              onclick: function() {
                return c.buildPDF();
              }
            }, state.building() ? 'Building...' : 'Build PDF')
          ])
        ]);
      }
    }
  };

  window.state = state;

  m.mount(document.getElementById('event-search'), EventSearch);

  m.mount(document.getElementById('event-select'), EventSelect);

  m.mount(document.getElementById('event-arrange'), EventArrange);

  m.mount(document.getElementById('pdf-build'), PDFBuild);

}).call(this);
