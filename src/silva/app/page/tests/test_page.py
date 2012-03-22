

import unittest
from zope.component import queryUtility
from zope.interface.verify import verifyObject

from silva.app.page.interfaces import IPage
from silva.app.page.testing import FunctionalLayer
from silva.core.contentlayout.interfaces import IContentLayoutService


class ServiceTestCase(unittest.TestCase):
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()

    def test_page(self):
        factory = self.root.manage_addProduct['silva.app.page']
        factory.manage_addPage('page', 'Page')

        page = self.root._getOb('page', None)
        self.assertTrue(verifyObject(IPage, page))

    def test_service(self):
        # Service must be installed by default by the extension
        service = queryUtility(IContentLayoutService)
        self.assertNotEqual(service, None)
        self.assertTrue(verifyObject(IContentLayoutService, service))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ServiceTestCase))
    return suite
