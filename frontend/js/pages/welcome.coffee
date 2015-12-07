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
                    'event_type[]': state.selectedTypes()
                    date_start: Math.round(moment().add(1, 'days').valueOf() / 1000)
                    date_end: Math.round(moment().add(state.searchMonths(), 'months').valueOf() / 1000)
                    radius_unit: 'mi'
                    format: 'json'
                    limit: 100

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
                    m '.col-md-6', [
                        m 'label', 'I live in'
                        m 'br'
                        m 'input[type=text].form-control',
                            placeholder: 'Zip Code'
                            onchange: m.withAttr 'value', state.searchZip
                            value: state.searchZip()
                    ]
                    m '.col-md-6', [
                        m 'label', 'Show events for'
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
                m '.row', m '.col.md-12', [
                    m 'br'
                    m 'label', 'I want flyers for... (click to select)'
                    if state.available()
                        m '#event-types', _.chunk(state.available().event_types, 3).map (chunk) ->
                            m '.row', chunk.map (et) ->
                                m '.event-type.col-md-4',
                                    class: if _.contains(state.selectedTypes(), et.value) then 'selected' else ''
                                    onclick: -> state.selectedTypes(_.xor(state.selectedTypes(), [et.value]))
                                , m 'span',
                                    style: if _.contains(state.selectedTypes(), et.value) then 'background-color: ' + et.color else ''
                                , et.name
                    else
                        m '', 'Loading! Please wait...'
                ]
                m '.row', m '.col-md-12', [
                    m 'hr'
                    m 'button[type=submit].btn.btn-lg.btn-primary', [
                        m 'i.glyphicon.glyphicon-search'
                        ' Search'
                    ]
                ]
            ]
