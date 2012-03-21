
from five import grok

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass

from Products.Silva.VersionedContent import VersionedContent
from Products.Silva.Version import Version

from silva.core import conf as silvaconf
from silva.app.news.AgendaItem import AgendaItemContent
from silva.app.news.AgendaItem import AgendaItemContentVersion
from silva.app.news.AgendaItem import IAgendaItemSchema
from silva.core.contentlayout.interfaces import ITitledPage
from zeam.form import silva as silvaforms

from .interfaces import IAgendaPage, IAgendaPageVersion


class AgendaPageVersion(AgendaItemContentVersion, Version):
    security = ClassSecurityInfo()
    meta_type = 'Silva Agenda Page Version'
    grok.implements(IAgendaPageVersion)


InitializeClass(AgendaPageVersion)


class Page(AgendaItemContent, VersionedContent):
    """ A Silva Page represents a web page, supporting advanced
        inline editing and content layout.
    """
    security = ClassSecurityInfo()
    grok.implements(IAgendaPage)
    meta_type = 'Silva Agenda Page'
    silvaconf.icon('news/agenda.png')
    silvaconf.version_class(AgendaPageVersion)
    silvaconf.priority(-8)


InitializeClass(Page)


class PageAddForm(silvaforms.SMIAddForm):
    """Add form for an agenda page.
    """
    grok.context(IAgendaPage)
    grok.name(u'Silva Agenda Page')

    fields = silvaforms.Fields(ITitledPage, IAgendaItemSchema)
