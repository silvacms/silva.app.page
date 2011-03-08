from silva.core.contentlayout.tests import ContentLayoutTestCase

from layer import PageLayer

import silva.app.page

class PageTestCase(ContentLayoutTestCase.ContentLayoutTestCase):
    layer = PageLayer(silva.app.page,
                       zcml_file='configure.zcml')

    def setUp(self):
        super(PageTestCase, self).setUp()
        root = self.layer.get_application()
        self.page = self.add_page(root, 'page', 'Page')
        self.pa = self.add_page_asset(root, 'pageasset', 'Page Asset')
