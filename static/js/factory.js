// Generated by CoffeeScript 1.10.0
(function() {
  var EventSearch, EventSelect, PDFBuild, state;

  state = {
    searchZip: m.prop(null),
    searchRadius: m.prop(100),
    searching: m.prop(false),
    building: m.prop(false),
    events: m.prop([]),
    selected: m.prop([])
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
            m('.col-xs-1', m('input[type=checkbox].form-control', {
              checked: _.includes(state.selected(), e.id),
              onchange: function() {
                return state.selected(_.xor(state.selected(), [e.id]));
              }
            })), m('.col-xs-11', [m('.event-name', e.name), m('.event-time', e.start_dt), m('.event-venue', e.venue_name)])
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
          return m('div.panel.panel-default', [m('div.panel.panel-heading', '2. Select Events'), m('div.panel-body', m('.scrollable', state.events().map(c.renderEvent)))]);
        }
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
          var selected_events;
          selected_events = _.filter(state.events(), isSelected);
          state.building(true);
          m.redraw();
          return m.request({
            method: 'POST',
            url: 'build',
            data: {
              events: selected_events
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
          m('.panel-heading', '3. Select Template and Build'), m('.panel-body', [
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

  m.mount(document.getElementById('pdf-build'), PDFBuild);

}).call(this);
