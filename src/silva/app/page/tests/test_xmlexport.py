
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest

from silva.app.page.testing import FunctionalLayer
from silva.core.contentlayout.designs.registry import registry
from silva.core.contentlayout.blocks.text import TextBlock
from silva.core.contentlayout.blocks.slot import BlockSlot
from silva.core.contentlayout import interfaces
from Products.Silva.tests.test_xml_export import SilvaXMLTestCase
from Products.Silva.silvaxml.xmlexport import exportToString
from silva.core.interfaces import IPublicationWorkflow


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
            xml, 'test_export_page.silva.xml', globs=globals())

    def test_export_with_page_model(self):
        factory = self.base_folder.manage_addProduct['silva.core.contentlayout']
        factory.manage_addPageModel('pm', 'A Page Model')
        page_model = self.base_folder.pm
        version = page_model.get_editable()
        version.set_design(self.design)
        IPublicationWorkflow(page_model).publish()

        text_block = TextBlock()
        controller = getMultiAdapter((text_block, self.page_version, TestRequest()),
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
            xml, 'test_export_with_page_model.silva.xml', globs=globals())

