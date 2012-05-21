
from five import grok
from zope.interface import Interface

from Products.Silva.silvaxml.xmlimport import NS_SILVA_URI
from Products.Silva.silvaxml.xmlexport import VersionedContentProducer

from silva.app.page.page import Page, PageVersion
from silva.core.contentlayout.silvaxml import NS_URI
from silva.core.contentlayout.silvaxml.xmlexport import BasePageProducer


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
