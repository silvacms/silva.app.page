# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from Products.Silva.testing import SilvaLayer
import silva.app.page
import transaction


class SilvaPageLayer(SilvaLayer):
    default_packages = SilvaLayer.default_packages + [
        'silva.core.contentlayout',
        'silva.app.page'
        ]

    def _install_application(self, app):
        super(SilvaPageLayer, self)._install_application(app)
        app.root.service_extensions.install('silva.app.page')
        transaction.commit()

FunctionalLayer = SilvaPageLayer(silva.app.page)
