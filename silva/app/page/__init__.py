from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller
from zope.interface import Interface
from Acquisition import aq_base

silvaconf.extensionName("silva.app.page")
silvaconf.extensionTitle("Silva Page and Page Assets")
silvaconf.extension_depends(("silva.core.contentlayout","SilvaExternalSources"))

# register FileSystemSite directories
from Products.FileSystemSite.DirectoryView import registerDirectory
registerDirectory('views', globals())

from Products.Silva.install import add_fss_directory_view

class Installer(DefaultInstaller):
    """Installer for Page and Page Asset extension.
    """
    
    def install(self, root):
        super(Installer, self).install(root)
        from page import PageContainerPolicy
        cpr = root.service_containerpolicy
        cpr.register('Silva Page', PageContainerPolicy, -10)
        if not hasattr(root.service_views.aq_inner.aq_explicit, 'silva.app.page'):
            add_fss_directory_view(root.service_views, 'silva.app.page', __file__, 'views')
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
        
        if hasattr(aq_base(root.service_views), 'silva.app.page'):
            root.service_views.manage_delObjects['silva.app.page']

class IExtension(Interface):
    """Marker interface for our extension.
    """

install = Installer("silva.app.page", IExtension)