
PDFBuild =
    controller: ->
        isSelected = (e) ->
            return _.includes state.selected(), e.id

        return {
            layoutDescription: ->
                if state.layout()
                    l = _.find state.available().layouts, (av) -> av.id == state.layout()
                    return if l then l.description else 'Unknown layout... weird!'
                else
                    return 'Please select a layout for your flyer.'

            buildPDF: ->
                state.building true
                m.redraw()
                m.request
                    method: 'POST'
                    url: 'build'
                    data:
                        events: state.selected()
                        layout: state.layout()
                        template: "TestFlyer"
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
                    m 'hr'
                    m 'h4', 'Layout'
                    m 'select.form-control',
                        onchange: m.withAttr 'value', state.layout
                    , state.available().layouts.map (l) ->
                        m 'option',
                            value: l.id
                            selected: state.layout() == l.id
                        , l.name
                    m '.text-muted', c.layoutDescription()
                    m 'hr'
                    m 'button.btn.btn-primary',
                        class: if state.building() then 'disabled' else ''
                        onclick: -> c.buildPDF()
                    , if state.building() then 'Building...' else 'Build PDF'
                ]
            ]

