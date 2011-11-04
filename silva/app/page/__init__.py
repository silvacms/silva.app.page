
from zope.interface import Interface

from silva.core import conf as silvaconf
from silva.core.conf.installer import DefaultInstaller

silvaconf.extension_name("silva.app.page")
silvaconf.extension_title(u"Silva Page")
silvaconf.extension_depends(["Silva", "silva.core.contentlayout"])


class Installer(DefaultInstaller):
    """Installer for Page and Page Asset extension.
    """


class IExtension(Interface):
    """Marker interface for our extension.
    """


install = Installer("silva.app.page", IExtension)
