from nox.coreapps.pyrt.pycomponent import *
from nox.lib.core import *

from nox.webapps.coreui.authui import UISection, UIResource, Capabilities
from nox.webapps.coreui import coreui

class DBExplorerSec(UISection):
    isLeaf = False
    required_capabilities = set([ "viewdb" ])

    def __init__(self, component, persistent):
        if persistent:
            self.dbname = "cdb"
        else:
            self.dbname = "ndb"
        UISection.__init__(self, component, self.dbname.upper()+"Explorer")

    def render_GET(self, request):
        return self.render_tmpl(request, "dbexplorer.mako", dbname=self.dbname)

class dbexplorerui(Component):

    hidden = False

    def __init__(self, ctxt):
        Component.__init__(self, ctxt)
        self.coreui = None

    def configure(self, configuration):
        for param in configuration['arguments']:
            if param == 'hidden':
                self.hidden = True

    def install(self):
        Capabilities.register("viewdb", "Browse raw DB tables.", [])
        Capabilities.register("updatedb", "Update raw DB tables.", [])
        self.coreui = self.resolve(str(coreui.coreui))
        self.coreui.install_section(DBExplorerSec(self, persistent=True), self.hidden)
        self.coreui.install_section(DBExplorerSec(self, persistent=False), self.hidden)

    def getInterface(self):
        return str(dbexplorerui)

def getFactory():
    class Factory:
        def instance(self, ctxt):
            return dbexplorerui(ctxt)

    return Factory()