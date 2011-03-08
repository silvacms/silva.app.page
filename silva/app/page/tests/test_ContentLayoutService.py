from zope.component.interfaces import ComponentLookupError

from PageTestCase import PageTestCase

class ContentLayoutServiceTestCase(PageTestCase):
    # some components of the content layout service need to be tested
    # when an extension is actually installed
    
    def test_getSupportingMetaTypes(self):
        # Might need to adjust if additional products like Silva News are installed in these test cases
        # also needs to be moved to silva.app.page
        self.assertEquals(['Silva Page'], self.service.get_supporting_meta_types())
        
import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContentLayoutServiceTestCase))
    return suite
