#zope
from five import grok
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Persistence import Persistent

#silva
from Products.Silva import SilvaPermissions
from Products.Silva.VersionedContent import CatalogedVersionedContent
from Products.Silva.Version import CatalogedVersion
from silva.core.interfaces import IContainerPolicy
from silva.core import conf as silvaconf

from silva.core.contentlayout.contentlayout import ContentLayout
from interfaces import IPage, IPageVersion

class PageVersion(CatalogedVersion, ContentLayout):
    """ A version of a Silva Page (i.e. a web page) """
    security = ClassSecurityInfo()
    
    meta_type = 'Silva Page Version'
    grok.implements(IPageVersion)
    
    def __init__(self, id):
        super(PageVersion, self).__init__(id)
        ContentLayout.__init__(self, id)
InitializeClass(PageVersion)

class Page(CatalogedVersionedContent):
    """ A Silva Page represents a web page, supporting advanced
        inline editing and content layout."""

    security = ClassSecurityInfo()
    grok.implements(IPage)
    meta_type = 'Silva Page'
    silvaconf.icon('page.png')
    silvaconf.version_class(PageVersion)
    silvaconf.priority(-10)
InitializeClass(Page)


#XXXaaltepet - how to register this as a container policy?
class SilvaPagePolicy(Persistent):
    """A ContainerPolicy for Silva Pages"""
    grok.implements(IContainerPolicy)
    def createDefaultDocument(self, container, title):
        """create a Silva Page as the default document in
           the container"""
        container.manage_addProduct['Silva'].manage_addPage('index', title)
        container.index.sec_update_last_author_info()