from zExceptions import BadRequest

from silva.core.contentlayout.parts import ExternalSourcePart
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

        
import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PageAssetTestCase))
    return suite
