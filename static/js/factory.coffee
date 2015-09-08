state =
    searchZip: m.prop null
    searchRadius: m.prop 100
    searching: m.prop false
    building: m.prop false
    events: m.prop []
    selected: m.prop []

Shared =
    eventBody: (e) -> [
        m '.event-name', e.name
        m '.event-time', e.start_dt
        m '.event-venue', e.venue_name
    ]

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
                    m '.col-xs-10', Shared.eventBody e
                    m '.col-xs-2',
                        m 'button.btn.btn-success.btn-xs',
                            onclick: ->
                                state.selected _.xor(state.selected(), [e])
                        , 'Add'
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
                    m '.panel.panel-heading', '2. Select Events'
                    m '.panel-body', m '.scrollable',
                        state.events().map c.renderEvent
                ]

EventArrange =
    controller: ->
        removeEvent = (e) -> state.selected _.without(state.selected(), e)
        moveEvent = (e, move) ->
            sel = state.selected()
            i = _.indexOf sel, e
            sel.splice(i, 1)
            i = i + move
            if i < 0 then i = 0
            if i > sel.length then i = sel.length
            sel.splice(i, 0, e)
            state.selected sel

        return {
            renderEvent: (e) ->
                m '.event.row', [
                    m '.col-xs-10', Shared.eventBody e
                    m '.col-xs-2',
                        m 'button.btn.btn-default.btn-xs',
                            onclick: -> moveEvent e, -1
                        , '▲'
                        m 'br'
                        m 'button.btn.btn-danger.btn-xs',
                            onclick: -> removeEvent e
                        , 'X'
                        m 'br'
                        m 'button.btn.btn-default.btn-xs',
                            onclick: -> moveEvent e, 1
                        , '▼'
                ]
        }
    view: (c) ->
        if state.selected().length > 0
            return m '.panel.panel-default', [
                m '.panel.panel-heading', '3. Arrange events'
                m '.panel-body', m '.scrollable',
                    state.selected().map c.renderEvent
            ]

PDFBuild =
    controller: ->
        isSelected = (e) ->
            return _.includes state.selected(), e.id

        return {
            buildPDF: ->
                state.building true
                m.redraw()
                m.request
                    method: 'POST'
                    url: 'build'
                    data:
                        events: state.selected()
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
                m '.panel-heading', '4. Layout, Template and Build'
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
m.mount document.getElementById('event-arrange'), EventArrange
m.mount document.getElementById('pdf-build'), PDFBuild
