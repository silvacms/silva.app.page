from five import grok
from zope.interface import Interface

from Products.Silva.silvaxml.xmlimport import NS_SILVA_URI
from Products.Silva.silvaxml.xmlexport import (VersionedContentProducer,
                                               SilvaBaseProducer,
                                               theXMLExporter)
#from silva.app.page.pageasset import PageAsset, PageAssetVersion
from silva.app.page.page import Page, PageVersion

NS_CL = 'http://infrae.com/ns/silva-contentlayout'
theXMLExporter.registerNamespace('contentlayout', NS_CL)

class PageProducer(VersionedContentProducer):
    """Export a Silva Page object to XML."""
    grok.adapts(Page, Interface)

    def sax(self):
        self.startElementNS(NS_CL,
                            'page',
                            {'id': self.context.id})
        self.workflow()
        self.versions()
        self.endElementNS(NS_CL, 'page')

class ContentLayoutProducerMixin(object):
    """Mixin to export content layout xml"""

    def content_layout_xml(self):
        self.startElementNS(NS_CL, 'layout')
        self.handler.characters(self.context.get_layout_name())
        self.endElementNS(NS_CL, 'layout')
        for slot in self.context.content_slots.keys():
            for part in self.context.get_parts_for_slot(slot):
                cs = getattr(self.context, part.get_name())
                self.startElementNS(NS_CL, 'part')
                self.startElementNS(NS_CL, 'name')
                self.handler.characters(part.get_name())
                self.endElementNS(NS_CL, 'name')
                self.startElementNS(NS_CL, 'slot')
                self.handler.characters(slot)
                self.endElementNS(NS_CL, 'slot')
                self.startElementNS(NS_CL, 'config')
                for k,v in part.get_config().items():
                    self.startElementNS(NS_CL, k, {'type': getattr(cs.parameters, k).meta_type})
                    self.handler.characters(unicode(v))
                    self.endElementNS(NS_CL, k)
                self.endElementNS(NS_CL, 'config')
                self.endElementNS(NS_CL, 'part')

class PageVersionProducer(ContentLayoutProducerMixin, SilvaBaseProducer):
    """Export a version of a Silva Page object to XML."""
    grok.adapts(PageVersion, Interface)

    def sax(self):
        self.startElementNS(NS_SILVA_URI, 'content', {'version_id': self.context.id})
        self.metadata()
        self.content_layout_xml()
        self.endElementNS(NS_SILVA_URI, 'content')


# class PageAssetProducer(VersionedContentProducer):
#     """Export a Silva Page Asset object to XML."""
#     grok.adapts(PageAsset, Interface)

#     def sax(self):
#         self.startElementNS(NS_CL,
#                             'pageasset',
#                             {'id': self.context.id})
#         self.workflow()
#         self.versions()
#         self.endElementNS(NS_CL, 'pageasset')


# class PageAssetVersionProducer(SilvaBaseProducer):
#     """Export a version of a Silva Page Asset object to XML."""
#     grok.adapts(PageAssetVersion, Interface)

#     def sax(self):
#         self.startElementNS(NS_CL, 'content', {'version_id': self.context.id})
#         self.metadata()
#         self.startElementNS(NS_CL, 'name')
#         self.handler.characters(self.context.get_part_name())
#         self.endElementNS(NS_CL, 'name')
#         self.startElementNS(NS_CL, 'config')
#         cs = self.context._get_source(self.context.get_part_name())
#         for k,v in self.context.get_config().items():
#             self.startElementNS(NS_CL, k, {'type': getattr(cs.parameters, k).meta_type})
#             self.handler.characters(unicode(v))
#             self.endElementNS(NS_CL, k)
#         self.endElementNS(NS_CL, 'config')
#         self.endElementNS(NS_CL, 'content')


