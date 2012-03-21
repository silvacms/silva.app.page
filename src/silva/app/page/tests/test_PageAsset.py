from zExceptions import BadRequest
from DateTime import DateTime

from silva.core.contentlayout.parts import ExternalSourcePart
from silva.core.contentlayout.interfaces import (IPartFactory, IPartView)
from PageTestCase import PageTestCase

class PageAssetTestCase(PageTestCase):
    
    def setUp(self):
        super(PageAssetTestCase, self).setUp()
        self.login('manager')
        token = self.root.service_codesources.manage_copyObjects(["cs_toc"])
        self.root.manage_pasteObjects(token)
        self.login('chiefeditor') 
        self.cs_name = "cs_toc"
        
    def test_save_name(self):
        #test setting the name of an external source within the page asset
        p = self.pa
        e = p.get_editable()
        
        e.set_part_name(self.cs_name)
        #the name should exist (as the cs was copied to the root)
        self.assertEquals(self.cs_name, e.get_part_name())
        self.assertRaises(BadRequest, e.set_part_name, 'blah')
        
    def test_save_config(self):
        #test saving the config, and getting it back
        p = self.pa
        e = p.get_editable()
        config = {'paths':'pub1'}
        e.set_part_name(self.cs_name)
        e.set_config(config)
        self.assertEquals(config, e.get_config())
        self.assertRaises(TypeError, e.set_config, None)

    def test_NotImplementedMethods(self):
        #These should all raise a NotImplementedError

        p = self.pa
        e = p.get_editable()
        config = {'paths': 'pub'}
        e.set_part_name(self.cs_name)
        e.set_config(config)
        self.assertRaises(NotImplementedError, e.update_quota) 
        self.assertRaises(NotImplementedError, e.reset_quota)
        self.assertRaises(NotImplementedError, e.get_filename)
        self.assertRaises(NotImplementedError, e.get_file_size) 
        self.assertRaises(NotImplementedError, e.get_mime_type)

        
class TestRichTextAssets(PageTestCase):
    #tests to make sure rendered page assets generate the "correct"
    # urls to internal resources.
    # (when ContentLayout supports references, these tests should continue
    # to function correctly)
    
    def setUp(self):
        super(TestRichTextAssets, self).setUp()
        self.login('manager')
        token = self.root.service_codesources.manage_copyObjects(['cs_rich_text'])
        self.root.manage_pasteObjects(token)
        self.login('chiefeditor')
        self.cs_name = 'cs_rich_text'
        self.layout_name = 'silva.core.contentlayout.templates.OneColumn'
        
        now = DateTime()
        
        # place a obj in folder1 which will be linked to from
        # folder11 and folder2
        self.folder1 = self.add_publication(self.root, 'folder1', 'folder1')
        self.folder1_toc = self.addObject(self.folder1, 'AutoTOC', 
                                          'toc', title='toc')
        self.folder1_pa = self.add_page_asset(self.folder1, 'pa1', 'pa1')
        e = self.folder1_pa.get_editable()
        e.set_part_name(self.cs_name)
        text = """<div><a href="toc" id="toclink">toclink</a>
                        <a href="folder11/page11" id="pagelink">pagelink</a>
                   </div>"""
        e.set_config({'rich_text':text})
        self.folder1_pa.set_unapproved_version_publication_datetime(now)
        self.folder1_pa.approve_version()
        
        self.folder11 = self.add_publication(self.folder1, 'folder11', 
                                             'folder11')
        self.folder11_page = self.add_page(self.folder11, 'page11', 'page11')
        self.folder11_page.set_unapproved_version_publication_datetime(now)
        self.folder11_page.approve_version()
        
        self.folder2 = self.add_publication(self.root, 'folder2', 'folder2')
        self.folder2_pa = self.add_page_asset(self.folder2, 'pa2', 'pa2')
        e = self.folder2_pa.get_editable()
        e.set_part_name('cs_page_asset')
        e.set_config({'object_path':'../folder1/pa1'})
        self.folder2_pa.set_unapproved_version_publication_datetime(now)
        self.folder2_pa.approve_version()

        self.folder2_page = self.add_page(self.folder2, 'page2', 'page2')
        e = self.folder2_page.get_editable()
        e.switch_template(self.layout_name)
        e = self.folder2_page.get_editable()
        cs = getattr(self.root, 'cs_page_asset')
        factory = IPartFactory(cs)
        part = factory.create({'object_path':'pa2'})
        e.add_part_to_slot(part, 'maincontent')
        self.folder2_page.set_unapproved_version_publication_datetime(now)
        self.folder2_page.approve_version()  #publish

    def test_public_links(self):
        #a test to ensure that multiply-embedded relative links
        # actually resolve to the correct output when publically rendered
        # This tests a page with an embedded page asset, this page asset
        # points to another page asset (this one a rich text) in another
        # folder.  The rich text as two links, one to a sibling of the
        # rich text pa, one to a page in a child container.
        
        #if link resolution was not properly working, the generated links
        # might end up being relative (and hence incorrect)
        sb = self.layer.get_browser()
        sb.inspect.add('toclink', '//a[@id="toclink"]', type="link")
        sb.inspect.add('pagelink', '//a[@id="pagelink"]', type="link")
        sb.open('/root/folder2/page2')
        toclink = sb.get_link("toclink")
        self.assertEquals(toclink.click(), 200)
        
        sb.open('/root/folder2/page2')
        pagelink = sb.get_link("pagelink")
        self.assertEquals(pagelink.click(), 200)

import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PageAssetTestCase))
    suite.addTest(unittest.makeSuite(TestRichTextAssets))
    return suite
