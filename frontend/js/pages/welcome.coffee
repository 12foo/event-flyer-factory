moment = require 'moment'

exports.EventSearch =
    controller: ->
        return {
            performSearch: ->
                state.searching true
                m.redraw()
                data =
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

                if state.onlyParties() == 'yes' then data['event_type[]'] = 36

                m.request
                    method: 'GET'
                    url: 'events'
                    data: data
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
            }, [
                m '.row', [
                    m '.col-md-4', [
                        m 'label', 'I live in'
                        m 'br'
                        m 'input[type=text].form-control',
                            placeholder: 'Zip Code'
                            onchange: m.withAttr 'value', state.searchZip
                            value: state.searchZip()
                    ]
                    m '.col-md-4', [
                        m 'label', 'I want'
                        m 'br'
                        m 'select.form-control',
                            onchange: m.withAttr 'value', state.onlyParties
                        , [["no", "all events"], ["yes", "Debate Watch Parties"]].map (l) ->
                            m 'option',
                                value: l[0]
                                selected: state.onlyParties() == l[0]
                            , l[1]
                    ]
                    m '.col-md-4', [
                        m 'label', 'for the'
                        m 'br'
                        m 'select.form-control',
                            onchange: m.withAttr 'value', state.layout
                        , [[1, "next month"], [3, "next three months"], [6, "next half year"]].map (l) ->
                            m 'option',
                                value: l[0]
                                selected: state.searchMonths() == l[0]
                            , l[1]
                    ]
                ]
                m '.row', m '.col-md-12', [
                    m 'button[type=submit].btn.btn-lg.btn-primary', [
                        m 'i.glyphicon.glyphicon-search'
                        ' Search'
                    ]
                ]
            ]
