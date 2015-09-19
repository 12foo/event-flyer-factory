moment = require 'moment'

exports.EventSearch =
    controller: ->
        return {
            performSearch: ->
                state.searching true
                m.redraw()
                m.request
                    method: 'GET'
                    url: 'events'
                    data:
                        country: 'US'
                        orderby: 'zip_radius'
                        'zip_radius[0]': state.searchZip()
                        'zip_radius[1]': 100
                        'event_type[]': Object.keys(state.available().event_types)
                        date_start: Math.round(moment().add(1, 'days').valueOf() / 1000)
                        date_end: Math.round(moment().add(state.searchMonths(), 'months').valueOf() / 1000)
                        radius_unit: 'mi'
                        format: 'json'
                        limit: 100
                .then (r) ->
                    state.selected []
                    state.events r.results
                    state.searching false
                    window.wizard.movePage 1
        }

    view: (c) ->
        if state.searching()
            return m '.loading', [
                m 'img',
                    src: 'static/spinners/spinner-blue.gif'
                m 'p', 'Hang on! Finding events near you.'
            ]
        else
            return m 'form.form-inline', {
                onsubmit: (e) ->
                    e.preventDefault()
                    c.performSearch()
            }, m '.row', [
                m '.col-md-4', [
                    m 'label', 'I live in'
                    m 'br'
                    m 'input[type=text].form-control',
                        placeholder: 'Zip Code'
                        onchange: m.withAttr 'value', state.searchZip
                        value: state.searchZip()
                ]
                m '.col-md-4', [
                    m 'label', 'I want events for'
                    m 'br'
                    m 'select.form-control',
                        onchange: m.withAttr 'value', state.layout
                    , [[1, "the next month"], [3, "the next three months"], [6, "the next half year"]].map (l) ->
                        m 'option',
                            value: l[0]
                            selected: state.searchMonths() == l[0]
                        , l[1]
                ]
                m '.col-md-4', [
                    m 'button[type=submit].btn.btn-lg.btn-primary', [
                        m 'i.glyphicon.glyphicon-search'
                        ' Search'
                    ]
                ]
            ]
