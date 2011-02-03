#zope
from five import grok
from zope.component import getUtility

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Persistence import Persistent

#silva
from Products.Silva import SilvaPermissions
from Products.Silva.VersionedContent import VersionedContent
from Products.Silva.Version import Version
from silva.translations import translate as _
from silva.core.interfaces import IContainerPolicy
from silva.core import conf as silvaconf
from zeam.form import silva as silvaforms

from silva.core.contentlayout.contentlayout import ContentLayout
from silva.core.contentlayout.interfaces.schema import ITemplateSchema
from silva.app.page.interfaces import IPage, IPageVersion

class PageVersion(Version, ContentLayout):
    """ A version of a Silva Page (i.e. a web page) """
    
    security = ClassSecurityInfo()
    
    meta_type = 'Silva Page Version'
    grok.implements(IPageVersion)
    
    def __init__(self, id):
        super(PageVersion, self).__init__(id)
        ContentLayout.__init__(self, id)
InitializeClass(PageVersion)

class Page(VersionedContent):
    """ A Silva Page represents a web page, supporting advanced
        inline editing and content layout.
    """

    security = ClassSecurityInfo()
    grok.implements(IPage)
    meta_type = 'Silva Page'
    silvaconf.icon('page.png')
    silvaconf.version_class(PageVersion)
    silvaconf.priority(-10)
InitializeClass(Page)

class IPageAddSchema(silvaconf.interfaces.ITitledContent, ITemplateSchema):
    """Pages have rich titled content and also the content layout template"""

class PageAddView(silvaforms.SMIAddForm):
    """Add form for a page asset"""
    
    grok.context(IPage)
    grok.name(u'Silva Page')
    
    fields = silvaforms.Fields(IPageAddSchema)
    
    def update(self):
        #XXXaaltepet here we hide the template fields if not appropriate
        # for this content type
        pass

class PageContainerPolicy(Persistent):
    """A ContainerPolicy for Silva Pages"""
    
    grok.implements(IContainerPolicy)
    
    def createDefaultDocument(self, container, title):
        """create a Silva Page as the default document in
           the container
        """
        container.manage_addProduct['silva.app.page'].manage_addPage('index', 
                                                                     title)
