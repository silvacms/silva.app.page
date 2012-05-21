
from silva.app.page.testing import FunctionalLayer
from silva.core.contentlayout.designs.registry import registry
from Products.Silva.tests.test_xml_export import SilvaXMLTestCase
from Products.Silva.silvaxml.xmlexport import exportToString

class TestPageExport(SilvaXMLTestCase):

    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('exportbase', 'Export base')
        self.base_folder = self.root.exportbase
        factory = self.base_folder.manage_addProduct['silva.app.page']
        factory.manage_addPage('apage', 'Page')
        self.page = self.base_folder.apage.get_editable()
        self.design = registry.lookup_design_by_name('adesign')
        self.page.set_design(self.design)

    def test_export_page(self):
        xml, info = exportToString(self.base_folder)
        self.assertExportEqual(
                    xml, 'test_export_page.silvaxml', globs=globals())


