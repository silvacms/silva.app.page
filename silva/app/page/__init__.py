from zope.interface import Interface

from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller

silvaconf.extensionName("silva.app.page")
silvaconf.extensionTitle("Silva Page and Page Assets")
silvaconf.extension_depends(("silva.core.contentlayout","SilvaExternalSources"))

class Installer(DefaultInstaller):
    """Installer for Page and Page Asset extension.
    """
    
    def install(self, root):
        super(Installer, self).install(root)
        from page import PageContainerPolicy
        cpr = root.service_containerpolicy
        cpr.register('Silva Page', PageContainerPolicy, -10)
        reg = root.service_view_registry
        reg.register('edit', 'Silva Page Asset', 
                     ['edit','VersionedContent','PageAsset'])
        reg.register('edit', 'Silva Page', 
                     ['edit','VersionedContent','Page'])

    def uninstall(self, root):
        super(Installer, self).uninstall(root)
        cpr = root.service_containerpolicy
        cpr.unregister('Silva Page')
        
        reg = root.service_view_registry
        reg.unregister('edit', 'Silva Page Asset')
        reg.unregister('edit', 'Silva Page')

class IExtension(Interface):
    """Marker interface for our extension.
    """

install = Installer("silva.app.page", IExtension)