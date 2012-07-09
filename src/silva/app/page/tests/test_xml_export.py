
from datetime import datetime

from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest

from Products.Silva.silvaxml.xmlexport import exportToString
from Products.Silva.tests.test_xml_export import SilvaXMLTestCase
from silva.core.contentlayout import interfaces
from silva.core.contentlayout.blocks.slot import BlockSlot
from silva.core.contentlayout.blocks.text import TextBlock
from silva.core.contentlayout.designs.registry import registry
from silva.core.interfaces import IPublicationWorkflow

from ..news.blocks import NewsInfoBlock, AgendaInfoBlock
from ..testing import FunctionalLayer


class TestPageExport(SilvaXMLTestCase):

    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('editor')
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('exportbase', 'Export base')
        self.base_folder = self.root.exportbase
        factory = self.base_folder.manage_addProduct['silva.app.page']
        factory.manage_addPage('apage', 'Page')
        self.page = self.base_folder.apage
        self.page_version = self.page.get_editable()
        self.design = registry.lookup_design_by_name('adesign')
        assert self.design, 'design not found'
        self.page_version.set_design(self.design)

    def test_export_page(self):
        xml, _ = exportToString(self.base_folder)
        self.assertExportEqual(
            xml, 'test_export_page.silvaxml', globs=globals())

    def test_export_with_page_model(self):
        factory = self.base_folder.manage_addProduct['silva.core.contentlayout']
        factory.manage_addPageModel('pm', 'A Page Model')
        page_model = self.base_folder.pm
        version = page_model.get_editable()
        version.set_design(self.design)
        IPublicationWorkflow(page_model).publish()

        text_block = TextBlock(identifier='text block 1')
        controller = getMultiAdapter(
            (text_block, self.page_version, TestRequest()),
            interfaces.IBlockController)
        controller.text = "<div>text</div>"

        manager = interfaces.IBlockManager(version)
        manager.add('two', text_block)
        manager.add('two', BlockSlot())
        manager.add('one', BlockSlot())

        self.page_version.set_design(version)
        self.assertEquals(version, self.page_version.get_design())

        xml, _ = exportToString(self.base_folder)
        self.assertExportEqual(
            xml, 'test_export_with_page_model.silvaxml', globs=globals())


class TestExportNewsPage(SilvaXMLTestCase):

    layer = FunctionalLayer

    def setUp(self):
        # adding base folder
        self.root = self.layer.get_application()
        self.layer.login('editor')

        factory = self.root.manage_addProduct['silva.app.news']
        factory.manage_addNewsPublication('news', 'News')
        # Show agenda items in the filter.
        self.base_folder = self.root.news
        self.base_folder.filter.set_show_agenda_items(True)
        assert self.base_folder


    def test_export_news_info_page(self):
        # adding news page
        factory = self.base_folder.manage_addProduct['silva.app.page']
        factory.manage_addNewsPage('newspage', 'A News Page')
        self.news_page = self.base_folder.newspage
        assert self.news_page
        self.news_page_version = self.news_page.get_editable()
        self.design = registry.lookup_design_by_name('adesign')
        assert self.design, 'design not found'
        self.news_page_version.set_design(self.design)

        self.news_page_version.set_subjects(['all'])
        self.news_page_version.set_target_audiences(['generic'])
        self.news_page_version.set_display_datetime(
            datetime(2010, 9, 30, 10, 0, 0))

        # adding blocks
        block = NewsInfoBlock()
        manager = interfaces.IBlockManager(self.news_page_version)
        manager.add('one', block)

        xml, _ = exportToString(self.base_folder)
        self.assertExportEqual(
            xml, 'test_export_news_page.silvaxml', globs=globals())

    def test_export_agenda_info_page(self): 
        # adding agenda page
        factory = self.base_folder.manage_addProduct['silva.app.page']
        factory.manage_addAgendaPage('agendapage', 'An Agenda Page')
        self.agenda_page = self.base_folder.agendapage
        assert self.agenda_page
        self.agenda_page_version = self.agenda_page.get_editable()
        self.design = registry.lookup_design_by_name('adesign')
        assert self.design, 'design not found'
        self.agenda_page_version.set_design(self.design)

        # adding block
        block = AgendaInfoBlock()
        manager = interfaces.IBlockManager(self.agenda_page_version)
        manager.add('one', block)

        xml, _ = exportToString(self.base_folder)
        self.assertExportEqual(
            xml, 'test_export_agenda_page.silvaxml', globs=globals())
