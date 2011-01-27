from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller
from zope.interface import Interface

silvaconf.extensionName("silva.app.page")
silvaconf.extensionTitle("Silva Page and Page Assets")
silvaconf.extension_depends(("silva.core.contentlayout","SilvaExternalSources"))

class Installer(DefaultInstaller):
    """Installer for Page and Page Asset extension.
    """
    
    def install(self, root):
        from page import PageContainerPolicy
        cpr = root.service_containerpolicy
        cpr.register('Silva Page', PageContainerPolicy, -10)

    def uninstall(self, root):
        cpr = root.service_containerpolicy
        cpr.unregister('Silva Page')

class IExtension(Interface):
    """Marker interface for our extension.
    """

install = Installer("silva.app.page", IExtension)