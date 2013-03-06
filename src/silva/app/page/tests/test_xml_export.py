# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 Infrae. All rights reserved.
# See also LICENSE.txt

import unittest
from datetime import datetime

from Products.Silva.testing import TestRequest
from Products.Silva.tests.test_xml_export import SilvaXMLTestCase

from silva.core.contentlayout.interfaces import IBlockController, IBlockManager
from silva.core.contentlayout.blocks.slot import BlockSlot
from silva.core.contentlayout.blocks.text import TextBlock
from silva.core.contentlayout.designs.registry import registry
from silva.core.interfaces import IPublicationWorkflow
from zeam.component import getWrapper

from ..news.blocks import NewsInfoBlock, AgendaInfoBlock
from ..testing import FunctionalLayer


class PageXMLExportTestCase(SilvaXMLTestCase):

    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('editor')
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('base', 'Export base')
        factory = self.root.base.manage_addProduct['silva.app.page']
        factory.manage_addPage('page', 'Page')
        design = registry.lookup_design_by_name('adesign')
        version = self.root.base.page.get_editable()
        version.set_design(design)

    def test_export_page(self):
        exporter = self.assertExportEqual(
            self.root.base,
            'test_export_page.silvaxml')
        self.assertEqual(exporter.getZexpPaths(), [])
        self.assertEqual(exporter.getAssetPaths(), [])
        self.assertEqual(exporter.getProblems(), [])

    def test_export_with_page_model(self):
        factory = self.root.base.manage_addProduct['silva.core.contentlayout']
        factory.manage_addPageModel('model', 'A Page Model')

        model = self.root.base.model
        version = model.get_editable()
        version.set_design(registry.lookup_design_by_name('adesign'))
        IPublicationWorkflow(model).publish()

        page_version = self.root.base.page.get_editable()
        text_block = TextBlock(identifier='text block 1')
        controller = getWrapper(
            (text_block, page_version, TestRequest()),
            IBlockController)
        controller.text = "<div>text</div>"

        manager = IBlockManager(version)
        manager.add('two', text_block)
        manager.add('two', BlockSlot())
        manager.add('one', BlockSlot())

        page_version = self.root.base.page.get_editable()
        page_version.set_design(version)
        self.assertEquals(version, page_version.get_design())

        exporter = self.assertExportEqual(
            self.root.base,
            'test_export_with_page_model.silvaxml')
        self.assertEqual(exporter.getZexpPaths(), [])
        self.assertEqual(exporter.getAssetPaths(), [])
        self.assertEqual(exporter.getProblems(), [])


class NewsPageXMLExportTestCase(SilvaXMLTestCase):

    layer = FunctionalLayer

    def setUp(self):
        # adding base folder
        self.root = self.layer.get_application()
        self.layer.login('editor')

        factory = self.root.manage_addProduct['silva.app.news']
        factory.manage_addNewsPublication('news', 'News')
        self.root.news.filter.set_show_agenda_items(True)

    def test_export_news_info_page(self):
        # adding news page
        factory = self.root.news.manage_addProduct['silva.app.page']
        factory.manage_addNewsPage('newspage', 'A News Page')
        version = self.root.news.newspage.get_editable()
        design = registry.lookup_design_by_name('adesign')
        self.assertIsNotNone(design)
        self.assertIsNotNone(version)

        version.set_design(design)
        version.set_subjects(['all'])
        version.set_target_audiences(['generic'])
        version.set_display_datetime(datetime(2010, 9, 30, 10, 0, 0))

        # adding blocks
        IBlockManager(version).add('one', NewsInfoBlock())

        exporter = self.assertExportEqual(
            self.root.news,
            'test_export_news_page.silvaxml')
        self.assertEqual(exporter.getZexpPaths(), [])
        self.assertEqual(exporter.getAssetPaths(), [])
        self.assertEqual(exporter.getProblems(), [])

    def test_export_agenda_info_page(self):
        # adding agenda page
        factory = self.root.news.manage_addProduct['silva.app.page']
        factory.manage_addAgendaPage('agendapage', 'An Agenda Page')
        version = self.root.news.agendapage.get_editable()
        design = registry.lookup_design_by_name('adesign')
        self.assertIsNotNone(version)
        self.assertIsNotNone(design)

        version.set_design(design)

        # adding block
        IBlockManager(version).add('one', AgendaInfoBlock())

        exporter = self.assertExportEqual(
            self.root.news,
            'test_export_agenda_page.silvaxml')
        self.assertEqual(exporter.getZexpPaths(), [])
        self.assertEqual(exporter.getAssetPaths(), [])
        self.assertEqual(exporter.getProblems(), [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PageXMLExportTestCase))
    suite.addTest(unittest.makeSuite(NewsPageXMLExportTestCase))
    return suite
