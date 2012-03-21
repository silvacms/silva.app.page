
from zope.interface import Interface
from zope.component import queryUtility

from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller
from silva.core.contentlayout.interfaces import IContentLayoutService

silvaconf.extension_name("silva.app.page")
silvaconf.extension_title(u"Silva Page")
silvaconf.extension_depends(["Silva", "silva.core.contentlayout"])


class PageInstaller(DefaultInstaller):
    """Installer for Page and Page Asset extension.
    """

    def install_custom(self, root):
        if queryUtility(IContentLayoutService) is None:
            factory = root.manage_addProduct['silva.core.contentlayout']
            factory.manage_addContentLayoutService()


class IExtension(Interface):
    """Marker interface for our extension.
    """


install = PageInstaller("silva.app.page", IExtension)
