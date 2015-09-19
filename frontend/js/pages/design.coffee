state = require 'state'

buildPDF = (layout) ->
    m.request
        method: 'POST'
        url: 'build'
        data:
            events: state.selected()
            layout: layout
            template: state.template()
    .then (r) ->
        if r.download
            window.wizard.movePage 1
            window.location.href = 'download/' + r.download
        else
            # error

exports.DesignSelect =
    controller: ->
    view: (c) ->
        if not state.template()
            return _.chunk(state.available().templates, 4).map (row) ->
                m '.row', row.map (tplname) ->
                    m '.item.col-sm-3',
                        onclick: -> state.template tplname
                    , [
                        m 'img',
                            src: 'preview/' + tplname + '/preview.jpg'
                        m 'p', tplname
                    ]
        else
            return _.chunk(state.available().layouts, 4).map (row) ->
                m '.row', row.map (layout) ->
                    m '.item.col-sm-3',
                        onclick: -> buildPDF layout.id
                    , [
                        m 'img',
                            src: 'preview/' + state.template() + '/' + layout.id + '/preview.jpg'
                        m 'p', layout.name
                    ]
