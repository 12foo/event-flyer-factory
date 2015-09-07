state =
    searchZip: m.prop null
    searchRadius: m.prop 100
    searching: m.prop false
    building: m.prop false
    events: m.prop []
    selected: m.prop []

EventSearch =
    controller: ->
        return {
            performSearch: ->
                state.searching true
                m.redraw()
                m.request
                    method: 'GET'
                    url: 'events/' + state.searchZip() + '/' + state.searchRadius() + '&country=US&radius_unit=mi&format=json'
                .then (r) ->
                    state.selected []
                    state.events r.results
                    state.searching false
        }

    view: (c) ->
        m 'div.panel.panel-default', [
            m 'div.panel-heading', '1. Search for Events'
            m 'div.panel-body', m 'form.form-inline', {
                onsubmit: (e) ->
                    e.preventDefault()
                    c.performSearch()
            }, m '.row', [
                m '.col-md-4', [
                    m 'input[type=text].form-control',
                        placeholder: 'Zip Code'
                        onchange: m.withAttr 'value', state.searchZip
                        value: state.searchZip()
                ]
                m '.col-md-4', [
                    m 'input[type=text].form-control',
                        placeholder: 'Radius (m)'
                        onchange: m.withAttr 'value', state.searchRadius
                        value: state.searchRadius()
                ]
                m '.col-md-4', [
                    m 'button[type=submit].btn.btn-primary', 'Search'
                ]
            ]
        ]

EventSelect =
    controller: ->
        return {
            renderEvent: (e) ->
                m '.event.row', [
                    m '.col-xs-1',
                        m 'input[type=checkbox].form-control',
                            checked: _.includes state.selected(), e.id
                            onchange: ->
                                state.selected _.xor(state.selected(), [e.id])
                    m '.col-xs-11', [
                        m '.event-name', e.name
                        m '.event-time', e.start_dt
                        m '.event-venue', e.venue_name
                    ]
                ]
        }
    view: (c) ->
        if state.searching()
                return m '.text-muted.center', 'Searching! Please wait...'
        else
            if state.events().length == 0
                return m '.text-muted.center', 'No results. Perform a search above.'
            else
                return m 'div.panel.panel-default', [
                    m 'div.panel.panel-heading', '2. Select Events'
                    m 'div.panel-body', m '.scrollable',
                        state.events().map c.renderEvent
                ]

PDFBuild =
    controller: ->
        isSelected = (e) ->
            return _.includes state.selected(), e.id

        return {
            buildPDF: ->
                selected_events = _.filter state.events(), isSelected
                state.building true
                m.redraw()
                m.request
                    method: 'POST'
                    url: 'build'
                    data:
                        events: selected_events
                .then (r) ->
                    state.building false
                    if r.download
                        window.location.href = 'download/' + r.download
                    else
                        # error

        }
    view: (c) ->
        if state.selected().length > 0
            return m '.panel.panel-default', [
                m '.panel-heading', '3. Select Template and Build'
                m '.panel-body', [
                    m '', state.selected().length + ' events selected.'
                    m 'button.btn.btn-primary',
                        class: if state.building() then 'disabled' else ''
                        onclick: -> c.buildPDF()
                    , if state.building() then 'Building...' else 'Build PDF'
                ]
            ]


window.state = state

m.mount document.getElementById('event-search'), EventSearch
m.mount document.getElementById('event-select'), EventSelect
m.mount document.getElementById('pdf-build'), PDFBuild
