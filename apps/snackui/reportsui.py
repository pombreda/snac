from nox.apps.pyrt.pycomponent import *
from nox.lib.core import *

from nox.apps.coreui.authui import UISection, UIResource, Capabilities
from nox.apps.user_event_log.UI_user_event_log import UI_user_event_log
from nox.apps.coreui import coreui

class ReportsSec(UISection):
    isLeaf = False
    required_capabilities = set([ "viewreports" ])

    def __init__(self, component):
        UISection.__init__(self, component, "Reports", "reportsButtonIcon")

    def render_GET(self, request):
        return self.render_tmpl(request, "reports.mako")

class reportsui(Component):

    def __init__(self, ctxt):
        Component.__init__(self, ctxt)
        self.coreui = None

    def install(self):
        Capabilities.register("viewreports", "View reports of past activity.",
                              ["Policy Administrator",
                               "Network Operator",
                               "Security Operator",
                               "Viewer"])
        self.coreui = self.resolve(str(coreui.coreui))
        self.coreui.install_section(ReportsSec(self))

    def getInterface(self):
        return str(reportsui)

def getFactory():
    class Factory:
        def instance(self, ctxt):
            return reportsui(ctxt)

    return Factory()
