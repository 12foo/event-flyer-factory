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
                m '.row', row.map (tpl) ->
                    m '.col-sm-3', m '.item',
                        onclick: ->
                            state.template tpl.id
                            # if template only has one layout, immediately select that and build
                            if tpl.layouts.length == 1
                                buildPDF tpl.layouts[0].id
                    , [
                        m 'img',
                            src: 'preview/' + tpl.id + '/preview.jpg'
                        m 'p.name', tpl.name
                        m 'p.creator', [
                            m 'span.by', 'by '
                            if tpl.link
                                m 'a.creator', href: tpl.link, tpl.creator
                            else
                                m 'span.creator', tpl.creator
                        ]
                    ]
        else
            return _.chunk(state.available().layouts, 4).map (row) ->
                m '.row', row.map (layout) ->
                    m '.col-sm-3', m '.item',
                        onclick: -> buildPDF layout.id
                    , [
                        m 'img',
                            src: 'preview/' + state.template() + '/' + layout.id + '/preview.jpg'
                        m 'p', layout.name
                    ]
