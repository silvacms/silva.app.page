
from five import grok
from zope.component import getMultiAdapter

from AccessControl import ClassSecurityInfo
from AccessControl.security import checkPermission
from App.class_init import InitializeClass

from Products.Silva.VersionedContent import VersionedContent
from Products.Silva.Version import Version

from silva.app.page.interfaces import IPage, IPageVersion
from silva.core import conf as silvaconf
from silva.core.contentlayout.interfaces import ITitledPage
from silva.core.smi.content import ContentEditMenu
from silva.core.smi.content import IEditScreen
from silva.core.views import views as silvaviews
from silva.core.views.interfaces import ISilvaURL
from silva.translations import translate as _
from silva.ui.menu import MenuItem
from silva.ui.rest.base import Screen, PageREST
from zeam.form import silva as silvaforms


class PageVersion(Version):
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



class IPageSchema(ITitledPage):
    pass



class PageAddForm(silvaforms.SMIAddForm):
    """Add form for a page asset"""

    grok.context(IPage)
    grok.name(u'Silva Page')

    fields = silvaforms.Fields(IPageSchema)


class PageEdit(PageREST):
    grok.adapts(Screen, IPage)
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


class PageDetailsForm(silvaforms.SMIEditForm):
    grok.context(IPage)
    grok.name('details')

    label = _(u"Page details")
    fields = silvaforms.Fields(IPageSchema).omit('id')


class PageDetailsMenu(MenuItem):
    grok.adapts(ContentEditMenu, IPage)
    grok.require('silva.ChangeSilvaContent')
    grok.order(15)

    name = _('Details')
    screen = PageDetailsForm


class PageView(silvaviews.View):
    grok.context(IPage)

    def render(self):
        template = self.content.template(self.content, self.request)
        return template()
