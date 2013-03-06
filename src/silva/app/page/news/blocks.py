# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 Infrae. All rights reserved.
# See also LICENSE.txt

from five import grok
from grokcore.chameleon.components import ChameleonPageTemplate
from zope.cachedescriptors.property import CachedProperty
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.browser import absoluteURL

from silva.app.news.interfaces import IServiceNews
from silva.core.contentlayout.blocks import Block, BlockController
from silva.translations import translate as _
from silva.ui.rest import UIREST

from .interfaces import INewsPageVersion, IAgendaPageVersion


class NewsInfoBlock(Block):
    grok.context(INewsPageVersion)
    grok.name('news-information')
    grok.title(_(u'News information'))
    grok.order(50)


class AgendaInfoBlock(Block):
    grok.context(IAgendaPageVersion)
    grok.name('agenda-information')
    grok.title(_(u'Agenda information'))
    grok.order(50)


class NewsInfoBlockController(BlockController):
    grok.adapts(NewsInfoBlock, INewsPageVersion, IHTTPRequest)

    template = ChameleonPageTemplate(filename="templates/newsinfo.cpt")

    def __init__(self, block, version, request):
        self.version = version
        self.request = request

    @CachedProperty
    def url(self):
        return absoluteURL(self.version.get_content(), self.request)

    @CachedProperty
    def format_date(self):
        return getUtility(IServiceNews).format_date

    @CachedProperty
    def publication_date(self):
        date = self.version.get_display_datetime()
        if date:
            return self.format_date(date)
        return u''

    def default_namespace(self):
        return {}

    def namespace(self):
        return {'version': self.version,
                'request': self.request,
                'view': self}

    def render(self, view=None):
        if view is None or view.final:
            return self.template.render(self)
        return _(u"This component is not available in this context.")


class AgendaInfoBlockController(NewsInfoBlockController):
    grok.adapts(AgendaInfoBlock, IAgendaPageVersion, IHTTPRequest)

    template = ChameleonPageTemplate(filename="templates/agendainfo.cpt")

    def occurrences(self):
        for occurrence in self.version.get_occurrences():
            timezone = occurrence.get_timezone()
            yield {
                'start': self.format_date(
                    occurrence.get_start_datetime(timezone),
                    occurrence.is_all_day()),
                'end': self.format_date(
                    occurrence.get_end_datetime(timezone),
                    occurrence.is_all_day()),
                'location': occurrence.get_location()}


class AddBlockREST(UIREST):
    grok.baseclass()
    grok.name('add')
    grok.require('silva.ChangeSilvaContent')

    message = _(u'Component created.')
    autoclose = 4000

    def __init__(self, context, request, configuration, restriction):
        super(AddBlockREST, self).__init__(context, request)
        self.configuration = configuration
        self.restriction = restriction

    def _create_block(self):
        raise NotImplementedError

    def GET(self):
        adding = self.__parent__
        adding.add(self._create_block())
        notify(ObjectModifiedEvent(self.context))

        return self.json_response({
                'content' : {
                    'extra': {
                        'block_id': adding.block_id,
                        'block_data': adding.block_controller.render(),
                        'block_editable': False},
                    'success': True},
                "notifications": [{
                        "category": "",
                        "message": self.message,
                        "autoclose": self.autoclose}],
                })


class AddNewsBlockREST(AddBlockREST):
    grok.adapts(NewsInfoBlock, INewsPageVersion)

    message = _(u'News information component added.')

    def _create_block(self):
        return NewsInfoBlock()


class AddAgendaBlockREST(AddBlockREST):
    grok.adapts(AgendaInfoBlock, IAgendaPageVersion)

    message = _(u'Agenda information component added.')

    def _create_block(self):
        return AgendaInfoBlock()
