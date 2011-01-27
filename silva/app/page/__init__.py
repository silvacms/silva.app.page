from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller
from zope.interface import Interface

silvaconf.extensionName("silva.app.page")
silvaconf.extensionTitle("Silva Page and Page Assets")
silvaconf.extension_depends(("silva.core.contentlayout","SilvaExternalSources"))

class IExtension(Interface):
    """Marker interface for our extension.
    """

install = DefaultInstaller("silva.app.page", IExtension)