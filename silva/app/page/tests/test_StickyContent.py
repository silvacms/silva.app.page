from zope.component.interfaces import ComponentLookupError

from DateTime import DateTime

from silva.core.interfaces import ISiteManager
from silva.core.contentlayout.parts import ExternalSourcePart
from silva.core.contentlayout.interfaces import IStickySupport

from PageTestCase import PageTestCase

class StickyContentTestCase(PageTestCase):
    # some components of the sticky content service need to be tested
    # when this extension is actually installed (since they require a
    # page asset
    
    def setUp(self):
        super(StickyContentTestCase, self).setUp()
        #the root service is added during Silva install
        self.root_service = self.root.service_sticky_content
        
        #make pub1 a local site so it can contain a sticky content service
        ISiteManager(self.pub1).makeSite()
        self.pub1.manage_addProduct['silva.core.contentlayout'].manage_addStickyContentService()
        self.pub1_service = self.pub1.service_sticky_content
        
        self.t_name = "silva.core.contentlayout.templates.OneColumn"
        self.slotname = 'maincontent'

        self.root_pa = self.add_page_asset(self.pub1, "root_pa", "Page Asset")
        pa_e = self.root_pa.get_editable()
        pa_e.set_part_name('cs_toc')
        pa_e.set_config({'paths':'/'.join(self.root.getPhysicalPath())})
        self.root_pa.set_unapproved_version_publication_datetime(DateTime()-1)
        self.root_pa.approve_version()

    def createPart(self, asset, placement="above"):
        #create and return a Sticky ContentPart
        return ExternalSourcePart('cs_page_asset',
                                  { "object_path":'/'.join(asset.getPhysicalPath()),
                                    "placement":placement
                                  })

    def test_sticky_rendering(self):
        #test sticky content rendering within a template.  If the sticky content
        # rendering fails, the page will have a <div class="warning"> on it.

        part = self.createPart(self.root_pa)
        part = self.root_service.addStickyContent(self.t_name, part, self.slotname)
        
        editable = self.page.get_editable()
        editable.switch_template(self.t_name)
        self.page.set_unapproved_version_publication_datetime(DateTime()-1)
        self.page.approve_version()  #publish
        
        sb = self.layer.get_browser()
        sb.options.handle_errors = False
        sb.open('/'.join(self.page.getPhysicalPath()))
        self.assertEquals(sb.status_code, 200)
        
        sb.inspect.add('parterror', '//div[@class="warning"]')
        self.assertEquals(sb.inspect.parterror, [])

import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StickyContentTestCase))
    return suite
