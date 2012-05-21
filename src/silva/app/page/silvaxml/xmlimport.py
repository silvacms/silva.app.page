
from silva.core import conf as silvaconf
from Products.Silva.silvaxml import xmlimport, NS_SILVA_URI
from silva.core.contentlayout.silvaxml import NS_URI
from silva.core.contentlayout.silvaxml.xmlimport import DesignHandler

silvaconf.namespace(NS_URI)


class PageHandler(xmlimport.SilvaBaseHandler):
    silvaconf.name('page')

    def getOverrides(self):
        return {(NS_SILVA_URI, 'content'): PageVersionHandler}

    def startElementNS(self, name, qname, attrs):
        if name == (NS_URI, 'page'):
            uid = self.generateOrReplaceId(attrs[(None, 'id')].encode('utf-8'))
            factory = self.parent().manage_addProduct[
                'silva.core.contentlayout']
            factory.manage_addPage(uid, '', no_default_version=True)
            self.setResultId(uid)

    def endElementNS(self, name, qname):
        if name == (NS_URI, 'page'):
            self.notifyImport()


class PageVersionHandler(xmlimport.SilvaBaseHandler):

    def getOverrides(self):
        return {(NS_URI, 'design'): DesignHandler}

    def startElementNS(self, name, qname, attrs):
        if (NS_SILVA_URI, 'content') == name:
            uid = attrs[(None, 'version_id')].encode('utf-8')
            factory = self.parent().manage_addProduct[
                'silva.core.contentlayout']
            factory.manage_addPageVersion(uid, '')
            self.setResultId(uid)

    def endElementNS(self, name, qname):
        if (NS_SILVA_URI, 'content') == name:
            xmlimport.updateVersionCount(self)
            self.storeMetadata()
            self.storeWorkflow()

