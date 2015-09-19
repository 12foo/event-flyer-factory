state = require 'state'

steps = ["Welcome", "Events", "Design", "Print"]

module.exports =
    controller: ->
    view: (c) ->
        elements = steps.map (title, step) ->
            cls = ''
            if state.page() == step then cls += 'active'
            if state.page() > step then cls += 'past'
            return m '.step',
                class: cls
            , [
                m 'h2', step + 1
                m 'div', title
            ]
        elements.reverse()
        m '.progress-steps', elements
