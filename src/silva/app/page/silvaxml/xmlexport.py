
from five import grok
from zope.interface import Interface

from Products.Silva.silvaxml.xmlimport import NS_SILVA_URI
from Products.Silva.silvaxml.xmlexport import VersionedContentProducer,\
    SilvaProducer

from silva.core.contentlayout.silvaxml import NS_URI
from silva.core.contentlayout.silvaxml.xmlexport import BasePageProducer
from silva.app.page.page import Page, PageVersion
from silva.app.page.news.news import NewsPage
from silva.app.page.news.news import NewsPageVersion
from silva.app.news.silvaxml.xmlexport import NewsItemVersionProducer
from silva.app.news.silvaxml.xmlexport import AgendaItemVersionProducer
from silva.app.page.news.agenda import AgendaPage, AgendaPageVersion
from silva.app.page.news.blocks import AgendaInfoBlock, NewsInfoBlock


class PageProducer(VersionedContentProducer):
    """Export a Silva Page object to XML."""
    grok.adapts(Page, Interface)

    def sax(self):
        self.startElementNS(NS_URI, 'page', {'id': self.context.id})
        self.workflow()
        self.versions()
        self.endElementNS(NS_URI, 'page')


class PageVersionProducer(BasePageProducer):
    """Export a version of a Silva Page object to XML."""
    grok.adapts(PageVersion, Interface)

    def sax(self):
        self.startElementNS(NS_SILVA_URI, 'content',
                            {'version_id': self.context.id})
        self.metadata()
        self.design()
        self.endElementNS(NS_SILVA_URI, 'content')


class NewsPageProducer(VersionedContentProducer):
    """Export a News item Page object to XML."""
    grok.adapts(NewsPage, Interface)

    def sax(self):
        self.startElementNS(NS_URI, 'newspage', {'id': self.context.id})
        self.workflow()
        self.versions()
        self.endElementNS(NS_URI, 'newspage')


class NewsPageVersionProducer(NewsItemVersionProducer, BasePageProducer):
    """ Export news item page version to XML
    """
    grok.adapts(NewsPageVersion, Interface)

    def extra_content(self):
        self.design()


class AgendaPageProducer(VersionedContentProducer):
    """ Export Agenda Page to XML
    """
    grok.adapts(AgendaPage, Interface)

    def sax(self):
        self.startElementNS(NS_URI, 'agendapage', {'id': self.context.id})
        self.workflow()
        self.versions()
        self.endElementNS(NS_URI, 'agendapage')


class AgendaPageVersionProducer(AgendaItemVersionProducer, BasePageProducer):
    """ Export Agenda Page Version to XML
    """
    grok.adapts(AgendaPageVersion, Interface)

    def extra_content(self):
        self.design()


class NewsInfoBlockProducer(SilvaProducer):
    """ Export AgendaInfoBlock to XML
    """
    grok.adapts(NewsInfoBlock, Interface)

    def sax(self, parent=None):
        self.startElementNS(NS_URI, 'newsinfoblock')
        self.endElementNS(NS_URI, 'newsinfoblock')


class AgendaInfoBlockProducer(SilvaProducer):
    """ Export AgendaInfoBlock to XML
    """
    grok.adapts(AgendaInfoBlock, Interface)

    def sax(self, parent=None):
        self.startElementNS(NS_URI, 'agendainfoblock')
        self.endElementNS(NS_URI, 'agendainfoblock')

