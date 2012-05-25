
from silva.core import conf as silvaconf
from Products.Silva.silvaxml import xmlimport, NS_SILVA_URI
from silva.app.news.silvaxml import helpers
from silva.core.contentlayout.silvaxml import NS_URI
from silva.app.news.silvaxml.xmlimport import NewsItemVersionHandler,\
    AgendaItemVersionHandler
from silva.core.contentlayout.silvaxml.xmlimport import DesignHandler,\
    BlockHandler
from silva.app.page.news.blocks import NewsInfoBlock, AgendaInfoBlock


silvaconf.namespace(NS_URI)


class PageHandler(xmlimport.SilvaBaseHandler):
    silvaconf.name('page')

    def getOverrides(self):
        return {(NS_SILVA_URI, 'content'): PageVersionHandler}

    def startElementNS(self, name, qname, attrs):
        if name == (NS_URI, 'page'):
            uid = self.generateOrReplaceId(attrs[(None, 'id')].encode('utf-8'))
            factory = self.parent().manage_addProduct[
                'silva.app.page']
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
                'silva.app.page']
            factory.manage_addPageVersion(uid, '')
            self.setResultId(uid)

    def endElementNS(self, name, qname):
        if (NS_SILVA_URI, 'content') == name:
            xmlimport.updateVersionCount(self)
            self.storeMetadata()
            self.storeWorkflow()


class NewsPageHandler(xmlimport.SilvaBaseHandler):
    silvaconf.name('newspage')

    def getOverrides(self):
        return {(NS_SILVA_URI, 'content'): NewsPageVersionHandler}

    def startElementNS(self, name, qname, attrs):
        if name == (NS_URI, 'newspage'):
            uid = self.generateOrReplaceId(attrs[(None, 'id')].encode('utf-8'))
            factory = self.parent().manage_addProduct['silva.app.page']
            factory.manage_addNewsPage(uid, '', no_default_version=True)
            self.setResultId(uid)

    def endElementNS(self, name, qname):
        if name == (NS_URI, 'newspage'):
            self.notifyImport()


class NewsPageVersionHandler(xmlimport.SilvaBaseHandler):

    def getOverrides(self):
        return {(NS_URI, 'design'): DesignHandler}

    def startElementNS(self, name, qname, attrs):
        if name == (NS_SILVA_URI, 'content'):
            uid = attrs[(None, 'version_id')].encode('utf-8')
            factory = self.parent().manage_addProduct['silva.app.page']
            factory.manage_addNewsPageVersion(uid, '')
            self.setResultId(uid)

            version = self.result()
            helpers.set_as_list(version, 'target_audiences', attrs)
            helpers.set_as_list(version, 'subjects', attrs)
            helpers.set_as_naive_datetime(version, 'display_datetime', attrs)

    def endElementNS(self, name, qname):
        if name == (NS_SILVA_URI, 'content'):
            xmlimport.updateVersionCount(self)
            self.storeMetadata()
            self.storeWorkflow()


class AgendaPageHandler(xmlimport.SilvaBaseHandler):
    silvaconf.name('agendapage')

    def getOverrides(self):
        return {(NS_SILVA_URI, 'content'): AgendaPageVersionHandler}

    def startElementNS(self, name, qname, attrs):
        if name == (NS_URI, 'agendapage'):
            uid = self.generateOrReplaceId(attrs[(None, 'id')].encode('utf-8'))
            factory = self.parent().manage_addProduct['silva.app.page']
            factory.manage_addAgendaPage(uid, '', no_default_version=True)
            self.setResultId(uid)

    def endElementNS(self, name, qname):
        if name == (NS_URI, 'agendapage'):
            self.notifyImport()


class AgendaPageVersionHandler(xmlimport.SilvaBaseHandler):

    def getOverrides(self):
        return {(NS_URI, 'design'): DesignHandler}

    def startElementNS(self, name, qname, attrs):
        if name == (xmlimport.NS_SILVA_URI, 'content'):
            uid = attrs[(None, 'version_id')].encode('utf-8')
            factory = self.parent().manage_addProduct['silva.app.page']
            factory.manage_addAgendaPageVersion(uid, '')
            self.setResultId(uid)

            version = self.result()
            helpers.set_as_list(version, 'target_audiences', attrs)
            helpers.set_as_list(version, 'subjects', attrs)
            helpers.set_as_naive_datetime(version, 'display_datetime', attrs)
            self.occurrences = []

    def endElementNS(self, name, qname):
        if name == (xmlimport.NS_SILVA_URI, 'content'):
            self.result().set_occurrences(self.occurrences)
            xmlimport.updateVersionCount(self)
            self.storeMetadata()
            self.storeWorkflow()


class NewsInfoBlockHandler(BlockHandler):
    silvaconf.name('newsinfoblock')

    def startElementNS(self, name, qname, attrs):
        if name == (NS_URI, 'newsinfoblock'):
            block = NewsInfoBlock()
            self._block = block

    def endElementNS(self, name, qname):
        if name == (NS_URI, 'newsinfoblock'):
            self.add_block(self._block)
            self._block = None


class AgendaInfoBlockHandler(BlockHandler):
    silvaconf.name('agendainfoblock')

    def startElementNS(self, name, qname, attrs):
        if name == (NS_URI, 'agendainfoblock'):
            block = AgendaInfoBlock()
            self._block = block

    def endElementNS(self, name, qname):
        if name == (NS_URI, 'agendainfoblock'):
            self.add_block(self._block)
            self._block = None

