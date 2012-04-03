
from five import grok
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.event import notify

from AccessControl import ClassSecurityInfo
from AccessControl.security import checkPermission
from App.class_init import InitializeClass

from Products.Silva.VersionedContent import VersionedContent
from Products.Silva.Version import Version

from silva.core import conf as silvaconf
from silva.core.contentlayout.interfaces import PageFields
from silva.core.contentlayout.interfaces import (IDesignLookup,
     DesignAssociatedEvent, DesignDeassociatedEvent)
from silva.core.smi.content import ContentEditMenu
from silva.core.smi.content import IEditScreen
from silva.core.views import views as silvaviews
from silva.core.views.interfaces import ISilvaURL
from silva.translations import translate as _
from silva.ui.menu import MenuItem
from silva.ui.rest.base import Screen, PageREST
from zeam.form import silva as silvaforms

from .interfaces import IPage, IPageVersion, IPageContent
from .interfaces import IPageContentVersion


class PageContentVersion(Version):
    grok.baseclass()
    grok.implements(IPageContentVersion)

    _design_name = None

    def get_design(self):
        service = getUtility(IDesignLookup)
        design = service.lookup_by_name(self._design_name)
        return design

    def set_design(self, design):
        previous = self.get_design()
        design_name = grok.name.bind().get(design)
        self._design_name = design_name
        if previous != design:
            if previous is not None:
                notify(DesignDeassociatedEvent(self, previous))
            if design is not None:
                notify(DesignAssociatedEvent(self, design))
        return design

    def fulltext(self):
        return [self.get_title()]


class PageVersion(PageContentVersion):
    """A version of a Silva Page (i.e. a web page)
    """
    security = ClassSecurityInfo()
    meta_type = 'Silva Page Version'
    grok.implements(IPageVersion)


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


class PageAddForm(silvaforms.SMIAddForm):
    """Add form for a page asset"""

    grok.context(IPage)
    grok.name(u'Silva Page')

    fields = PageFields


class PageEdit(PageREST):
    grok.adapts(Screen, IPageContent)
    grok.name('content')
    grok.implements(IEditScreen)
    grok.require('silva.ReadSilvaContent')

    def payload(self):
        if checkPermission('silva.ChangeSilvaContent', self.context):
            version = self.context.get_editable()
            if version is not None:
                return {"ifaces": ["content-layout"],
                        "path": version.getId()}

        url = getMultiAdapter((self.context, self.request), ISilvaURL).preview()
        return {"ifaces": ["preview"],
                "html_url": url}


class PageDesignForm(silvaforms.SMIEditForm):
    grok.context(IPageContent)
    grok.name('design')

    label = _(u"Page design")
    fields = PageFields.omit('id')


class PageDesignMenu(MenuItem):
    grok.adapts(ContentEditMenu, IPageContent)
    grok.require('silva.ChangeSilvaContent')
    grok.order(15)

    name = _('Design')
    screen = PageDesignForm


class PageView(silvaviews.View):
    grok.context(IPageContent)

    def render(self):
        design = self.content.get_design()
        render = design(self.content, self.request)
        return render()
