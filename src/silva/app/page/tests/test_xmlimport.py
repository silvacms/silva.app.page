
from Products.Silva.tests.test_xml_import import SilvaXMLTestCase
from ..testing import FunctionalLayer
from silva.app.page.page import Page, PageVersion
from silva.core.contentlayout.model import PageModelVersion
from silva.core.messages.interfaces import IMessageService
from zope.publisher.browser import TestRequest
from zope.component import getUtility
from silva.app.page.news.news import NewsPage, NewsPageVersion
from silva.app.page.news.agenda import AgendaPageVersion, AgendaPage


class TestPageImport(SilvaXMLTestCase):

    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('editor')

    def test_import_page(self):
        self.import_file("test_import_page.silva.xml",
                         globs=globals())
        base = self.root._getOb('exportbase')
        page = base._getOb('apage')
        self.assertIsInstance(page, Page)
        page_version = page.get_editable()
        self.assertIsInstance(page_version, PageVersion)
        design = page_version.get_design()
        self.assertTrue(design)

    def test_import_with_page_model(self):
        self.import_file("test_import_with_page_model.silva.xml",
                         globs=globals())

        message_service = getUtility(IMessageService)
        errors = message_service.receive(TestRequest(), namespace='error')
        self.assertEquals(0, len(errors),
            "import warning: " + "\n".join(map(str, errors)))

        base = self.root._getOb('exportbase')
        page = base._getOb('apage')
        self.assertIsInstance(page, Page)
        page_version = page.get_editable()
        self.assertIsInstance(page_version, PageVersion)
        page_model = page_version.get_design()
        self.assertIsInstance(page_model, PageModelVersion)

    def test_import_news_page(self):
        self.import_file("test_import_news_page.silva.xml", globs=globals())
        message_service = getUtility(IMessageService)
        errors = message_service.receive(TestRequest(), namespace='error')

        base = self.root._getOb('news')
        news_page = base._getOb('newspage')
        self.assertIsInstance(news_page, NewsPage)
        version = news_page.get_editable()
        self.assertIsInstance(version, NewsPageVersion)
        design = version.get_design()
        self.assertTrue(design)

        # XXX: add block test

    def test_import_agenda_page(self):
        self.import_file("test_import_agenda_page.silva.xml", globs=globals())
        message_service = getUtility(IMessageService)
        errors = message_service.receive(TestRequest(), namespace='error')

        base = self.root._getOb('news')
        agenda_page = base._getOb('agendapage')
        self.assertIsInstance(agenda_page, AgendaPage)
        version = agenda_page.get_editable()
        self.assertIsInstance(version, AgendaPageVersion)
        design = version.get_design()
        self.assertTrue(design)

        # XXX: add block test
