# -*- coding: utf-8 -*-
# Copyright (c) 2012  Infrae. All rights reserved.
# See also LICENSE.txt

from Products.Silva.tests.test_xml_import import SilvaXMLTestCase
from silva.app.page.news.agenda import AgendaPageVersion, AgendaPage
from silva.app.page.news.blocks import NewsInfoBlock, AgendaInfoBlock
from silva.app.page.news.news import NewsPage, NewsPageVersion
from silva.app.page.page import Page, PageVersion
from silva.core.contentlayout.interfaces import IBlockManager
from silva.core.contentlayout.model import PageModelVersion

from ..testing import FunctionalLayer


class TestPageImport(SilvaXMLTestCase):

    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('editor')

    def test_import_page(self):
        importer = self.assertImportFile(
            "test_import_page.silvaxml",
            ['/root/base',
             '/root/base/page'])
        self.assertEqual(importer.getProblems(), [])
        base = self.root._getOb('base')
        page = base._getOb('page')
        self.assertIsInstance(page, Page)
        page_version = page.get_editable()
        self.assertIsInstance(page_version, PageVersion)
        design = page_version.get_design()
        self.assertTrue(design)

    def test_import_with_page_model(self):
        importer = self.assertImportFile(
            "test_import_with_page_model.silvaxml",
            ['/root/base/page',
             '/root/base/model',
             '/root/base'])
        self.assertEqual(importer.getProblems(), [])

        base = self.root._getOb('base')
        page = base._getOb('page')
        self.assertIsInstance(page, Page)
        page_version = page.get_editable()
        self.assertIsInstance(page_version, PageVersion)
        page_model = page_version.get_design()
        self.assertIsInstance(page_model, PageModelVersion)
        self.assertIs(base._getOb('model')._getOb('0'), page_model)

    def test_import_news_page(self):
        importer = self.assertImportFile(
            "test_import_news_page.silvaxml",
            ['/root/news/index',
             '/root/news/newspage',
             '/root/news/filter',
             '/root/news'])
        self.assertEqual(importer.getProblems(), [])

        base = self.root._getOb('news')
        news_page = base._getOb('newspage')
        self.assertIsInstance(news_page, NewsPage)
        version = news_page.get_editable()
        self.assertIsInstance(version, NewsPageVersion)
        design = version.get_design()
        self.assertTrue(design)

        manager = IBlockManager(version)
        slot = manager.get_slot('one')
        _, block = slot[0]
        self.assertIsInstance(block, NewsInfoBlock)

    def test_import_agenda_page(self):
        importer = self.assertImportFile(
            "test_import_agenda_page.silvaxml",
            ['/root/news/index',
             '/root/news/agendapage',
             '/root/news/filter',
             '/root/news'])
        self.assertEqual(importer.getProblems(), [])

        base = self.root._getOb('news')
        agenda_page = base._getOb('agendapage')
        self.assertIsInstance(agenda_page, AgendaPage)
        version = agenda_page.get_editable()
        self.assertIsInstance(version, AgendaPageVersion)
        design = version.get_design()
        self.assertTrue(design)

        manager = IBlockManager(version)
        slot = manager.get_slot('one')
        _, block = slot[0]
        self.assertIsInstance(block, AgendaInfoBlock)
