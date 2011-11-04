from DateTime import DateTime

from Products.Silva.silvaxml.xmlimport import SilvaBaseHandler
from silva.core import conf as silvaconf
#from silva.app.page.pageasset import PageAsset, PageAssetVersion
#from silva.core.contentlayout.interfaces import IPartFactory

from silva.app.page.xmlexport import NS_CL

silvaconf.namespace(NS_CL)

class PageHandler(SilvaBaseHandler):
    silvaconf.name('page')
    def getOverrides(self):
        return {
            (NS_CL, 'content'): PageContentHandler
            }

    def startElementNS(self, name, qname, attrs):
        if name== (NS_CL, 'page'):
            uid = self.generateOrReplaceId(attrs[(None, 'id')].encode('utf-8'))
            folder = self.parent()
            factory = folder.manage_addProduct['silva.app.page']
            factory.manage_addPage(uid, '', no_default_version=True)
            last_author = attrs.get((None, 'last_author'),None)
            if last_author:
                self.setAuthor(getattr(self.parent(), uid), self.parent(),
                               last_author)
            self.setResultId(uid)

    def endElementNS(self, name, qname):
        if name == (NS_CL, 'page'):
            self.notifyImport()


class PageContentHandler(SilvaBaseHandler):
    def getOverrides(self):
        return {
            (NS_CL, 'part'): ContentLayoutPartHandler
            }
    
    def characters(self, chars):
        self._chars = chars

    def startElementNS(self, name, qname, attrs):
        if name == (NS_CL, 'content'):
            if attrs.has_key((None, 'version_id')):
                uid = attrs[(None, 'version_id')].encode('utf-8')
                factory = self.parent().manage_addProduct['silva.app.page']
                factory.manage_addPageVersion(uid, '')
                last_author = attrs.get((None, 'last_author'),None)
                if last_author:
                    self.setAuthor(getattr(self.parent(), uid), self.parent(),
                                   last_author)
                self.setResultId(uid)

    def endElementNS(self, name, qname):
        if name == (NS_CL, 'content'):
            self.storeMetadata()
            self.storeWorkflow()
        elif name == (NS_CL, 'layout'):
            self._result.switch_template(self._chars)


class ContentLayoutPartHandler(SilvaBaseHandler):
    def getOverrides(self):
        return {
            (NS_CL, 'config'): ConfigElementHandler
            }

    def characters(self, chars):
        self._chars = chars

    def startElementNS(self, name, qname, attrs):
        pass

    def endElementNS(self, name, qname):
        if name == (NS_CL, 'name'):
            cs = getattr(self.parent().aq_inner, self._chars)
            pf = IPartFactory(cs)
            self._part = pf.create({})
        elif name == (NS_CL, 'slot'):
            self.parent().add_part_to_slot(self._part, self._chars)
            self.setResult(self.parent().get_part(self._part.get_key()))


class ConfigElementHandler(SilvaBaseHandler):
    def getOverrides(self):
        return {}
    
    def characters(self, chars):
        self._chars = chars

    def startElementNS(self, name, qname, attrs):
        if name == (NS_CL, 'config'):
            self._config = {}
        else:
            self._type = attrs[(None, 'type')]
            self._chars = ''

    def endElementNS(self, name, qname):
        if name == (NS_CL, 'config'):
            self.parent().set_config(self._config)
        else:
            if self._type == 'DateTimeField':
                self._config[str(name[1])] = DateTime(self._chars)
            elif self._type in ('EmailLinesField', 'LinesField', \
                                'MultiCheckBoxField', 'MultiListField', 'PhoneField'):
                self._config[str(name[1])] = eval(self._chars)
            else:
                self._config[str(name[1])] = self._chars


# class PageAssetHandler(SilvaBaseHandler):
#     silvaconf.name('pageasset')
    
#     def getOverrides(self):
#         return {
#             (NS_CL, 'content'): PageAssetContentHandler
#             }

#     def startElementNS(self, name, qname, attrs):
#         if name == (NS_CL, 'pageasset'):
#             uid = self.generateOrReplaceId(attrs[(None, 'id')].encode('utf-8'))
#             factory = self.parent().manage_addProduct['silva.app.page']
#             factory.manage_addPageAsset(uid, '', no_default_version=True)
#             last_author = attrs.get((None, 'last_author'),None)
#             if last_author:
#                 self.setAuthor(getattr(self.parent(), uid), self.parent(),
#                                last_author)
#             self.setResultId(uid)

#     def endElementNS(self, name, qname):
#         if name == (NS_CL, 'pageasset'):
#             self.notifyImport()


# class PageAssetContentHandler(SilvaBaseHandler):
#     def getOverrides(self):
#         return {
#             (NS_CL, 'config'): ConfigElementHandler
#             }
    
#     def characters(self, chars):
#         self._chars = chars

#     def startElementNS(self, name, qname, attrs):
#         if name == (NS_CL, 'content'):
#             if attrs.has_key((None, 'version_id')):
#                 uid = attrs[(None, 'version_id')].encode('utf8')
#                 factory = self.parent().manage_addProduct['silva.app.page']
#                 factory.manage_addPageAssetVersion(uid, '')
#                 last_author = attrs.get((None, 'last_author'),None)
#                 if last_author:
#                     self.setAuthor(getattr(self.parent(), uid), self.parent(),
#                                    last_author)
#                 self.setResultId(uid)

#     def endElementNS(self, name, qname):
#         if name == (NS_CL, 'content'):
#             self.storeMetadata()
#             self.storeWorkflow()
#         elif name == (NS_CL, 'name'):
#             self._result.set_part_name(self._chars)

