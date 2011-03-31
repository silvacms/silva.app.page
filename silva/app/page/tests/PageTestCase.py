from silva.core.contentlayout.tests import ContentLayoutTestCase

import layer

import silva.app.page

class PageTestCase(ContentLayoutTestCase.ContentLayoutTestCase):
    layer = layer.FunctionalPageLayer
    #(silva.app.page,
#                       zcml_file='configure.zcml')

    def setUp(self):
        super(PageTestCase, self).setUp()
        self.page = self.add_page(self.root, 'page', 'Page')
        self.pa = self.add_page_asset(self.root, 'pageasset', 'Page Asset')
        self.pub1_pa = self.add_page_asset(self.root.pub, 'pageasset', 
                                           'Page Asset')

    def add_page_asset(self, object, id, title):
        return self.addObject(object, 'PageAsset', id, title=title,
                              product='silva.app.page')
      