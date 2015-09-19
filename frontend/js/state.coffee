# this module keeps global mithril application state

module.exports =
    page: m.prop 0
    searchZip: m.prop null
    searchMonths: m.prop 1
    searching: m.prop false
    events: m.prop []
    selected: m.prop []
    template: m.prop null
    available: m.prop null
