moment = require 'moment'

renderEvent = (e) ->
    t = moment(e.start_dt)
    return m '.event',
        key: e.id
        onclick: -> state.selected _.xor(state.selected(), [e])
    , [
        m 'span.event-type',
            style:
                background: state.typeMap()[e.type_id].color
        , state.typeMap()[e.type_id].name
        # m '.event-date', t.format('MMM D, YYYY h:mma ') + e.timezone + ' (' + t.fromNow() + ')'
        m '.event-date', t.format('MMM D, YYYY h:mma ') + e.timezone
        m 'h5.event-title', e.name
        m '.event-venue', _.compact([e.venue_name, e.venue_addr1, e.venue_city, e.venue_state_cd, e.venue_zip]).join(', ')
    ]

moveSelected = (e, d) ->
    sel = state.selected()
    i = _.indexOf(sel, e)
    sel.splice(i, 1)
    i = i + d
    if i < 0 then i = 0
    if i > sel.length then i = sel.length
    sel.splice(i, 0, e)
    state.selected sel

renderMovableEvent = (e, i, a) ->
    return m '.row.movable',
        key: e.id
    , [
        m '.col-xs-11.nopadding', renderEvent e
        m '.col-xs-1.nopadding.move-buttons', [
            if i > 0 then m 'button.up',
                onclick: -> moveSelected e, -1
            , m 'i.glyphicon.glyphicon-arrow-up'
            if i < a.length - 1 then m 'button.down',
                onclick: -> moveSelected e, 1
            , m 'i.glyphicon.glyphicon-arrow-down'
        ]
    ]

exports.EventSelect =
    controller: ->
    view: (c) ->
        return m '.row', [
            m '.col-xs-6.nopadding', [
                m 'h4.drag-header', 'Events near you'
                m '.event-selection', m '.scroll-content', _.xor(state.events(), state.selected()).map renderEvent
                m '.action.align-right', [
                    m 'span.big.white', ''
                ]
            ]
            m '.col-xs-6.nopadding', [
                m 'h4.drag-header', 'Events on your flyer'
                if state.selected().length > 0
                    m '.event-selection', m '.scroll-content', state.selected().map renderMovableEvent
                else
                    m '.event-selection', m '.well', "Tap an event to the left to add it to your flyer."
                m '.action.align-right', [
                    m 'span.big.white', 'Got everything?'
                    m 'button.btn.btn-primary',
                        onclick: -> window.wizard.movePage 1
                    , 'Next ➤'
                ]
            ]
        ]
