# Zope 3
from five import grok
from zope.app.container.interfaces import IObjectRemovedEvent
from persistent.mapping import PersistentMapping

# Zope 2
from zExceptions import BadRequest
from OFS import Folder
from OFS.interfaces import IObjectWillBeAddedEvent
from AccessControl import ClassSecurityInfo, getSecurityManager
from Globals import InitializeClass

from Products.Silva import SilvaPermissions
from Products.Silva.VersionedAsset import CatalogedVersionedAsset
from Products.Silva.Version import CatalogedVersion
from Products.SilvaExternalSources.interfaces import IExternalSource
from silva.core import conf as silvaconf
from zeam.form import silva as silvaforms

from interfaces import (IPageAsset, IPageAssetVersion)
#, IPartFactory
#from browser.interfaces import IContentLayoutPartEditWidget

class PageAssetVersion(CatalogedVersion):
    """A version of a Page Asset"""
    
    security = ClassSecurityInfo()
    
    grok.implements(IPageAssetVersion)
    
    meta_type = "Silva Page Asset Version"

    def __init__(self, id):
        """Initialize PageAsset"""
        PageAssetVersion.inheritedAttribute('__init__')(self, id)
        self._part = None

    def _getSource(self, esname):
        """private function to get the ExternalSource `esname`
           within the current context"""
        try:
            source = getattr(self.aq_inner,esname)
        except AttributeError:
            raise BadRequest()
        if not IExternalSource.providedBy(source):
            raise BadRequest()
        return source
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'setName')
    def setName(self, name):
        #ensure source is accessible, this will raise an error if not
        source = self._getSource(name)
        pf = IPartFactory(source)
        #create a part associated with the source, with an empty config
        # (since we don't have a config yet)
        self._part = pf.create({})

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'setConfig')
    def setConfig(self, config_dict):
        #convert config to a dict, then create a PersistentMapping
        # out of it.  
        d = PersistentMapping(dict(config_dict))
        self._part.setConfig(d)
        
    def getConfig(self):
        if not self._part:
            return None
        return self._part.getConfig(copy=True)
        
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'getName')
    def getName(self):
        if not self._part:
            return None
        return self._part.getName()
    
InitializeClass(PageAssetVersion)
    

class PageAsset(CatalogedVersionedAsset):
    """A Page Asset is a versioned instance of an External
       Source, which can be placed/reused on multiple Silva Pages."""
    
    meta_type = "Silva Page Asset"
    
    security = ClassSecurityInfo()
    
    grok.implements(IPageAsset)
    silvaconf.icon("pageasset.png")
    silvaconf.version_class(PageAssetVersion)
    
    def __init__(self, id):
        """Initialize PageAsset"""
        PageAsset.inheritedAttribute('__init__')(self, id)
        
InitializeClass(PageAsset)

class PageAssetAddView(silvaforms.SMIAddForm):
    """Add form for a a page asset"""
    grok.context(IPageAsset)
    grok.name(u'Silva Page Asset')
    
    fields = silvaforms.Fields(silvaconf.interfaces.IBasicTitledContent)