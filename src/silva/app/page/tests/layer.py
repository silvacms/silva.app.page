from silva.core.contentlayout.tests.layer import ContentLayoutLayer

import silva.app.page

class PageLayer(ContentLayoutLayer):

    def _install_application(self, app):
        """make sure silva page extension is installed"""
        
        super(PageLayer, self)._install_application(app)
        app.root.service_extensions.install("silva.app.page")

FunctionalPageLayer = PageLayer(silva.app.page)