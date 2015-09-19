state = require 'state'

window.state = state

# load available layouts/templates in the background
m.request
    method: 'GET'
    url: 'available'
    background: true
.then (av) ->
    state.available av
    state.layout av.layouts[0].id

# this controls display/moving between individual wizard pages
wizard =
    movePage: (direction) ->
        pages = document.getElementsByClassName 'wizard-page'
        current = pages[state.page()]
        next = pages[state.page() + direction]
        if not next then return
        next.className = 'wizard-page shown'
        current.className = 'wizard-page hidden'
        state.page state.page() + direction
    resize: ->
        max = window.innerHeight
        esHeight = max - 440
        wpHeight = max - 200
        [].forEach.call document.getElementsByClassName('wizard-page'), (e) ->
            e.style.height = wpHeight + "px"
        [].forEach.call document.getElementsByClassName('event-selection'), (e) ->
            e.style.height = esHeight + "px"

window.onresize = wizard.resize
window.wizard = wizard
setTimeout wizard.resize, 100

# uncomment this to test page 2 with sample events
# m.request({method: 'GET', url: 'static/test/test-events.json'}).then((te) -> state.events te.results; wizard.movePage 1)

# and this for page 3
# m.request({method: 'GET', url: 'static/test/test-events.json'}).then((te) -> state.events te.results; state.selected _.sample(te.results, 10); wizard.movePage 2)


# set up the pages after initial load
[].forEach.call document.getElementsByClassName('wizard-page'), (page) ->
    page.className = 'wizard-page hidden'

document.getElementsByClassName('wizard-page')[state.page()].className = 'wizard-page shown'

# mount pages and other elements
m.mount document.getElementById('progress-indicator'), require('progress')
m.mount document.getElementById('event-search'), require('pages/welcome').EventSearch
m.mount document.getElementById('event-select'), require('pages/select').EventSelect
m.mount document.getElementById('design-select'), require('pages/design').DesignSelect
