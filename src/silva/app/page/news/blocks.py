# -*- coding: utf-8 -*-
# Copyright (c) 2012-2013 Infrae. All rights reserved.
# See also LICENSE.txt

import localdatetime

from datetime import datetime
from five import grok
from grokcore.chameleon.components import ChameleonPageTemplate
from zope.cachedescriptors.property import CachedProperty
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.browser import absoluteURL

from silva.app.news.interfaces import IServiceNews
from silva.app.news.datetimeutils import RRuleData
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
            if not isinstance(date, datetime):
                date = date.asdatetime()
            local_months = localdatetime.get_month_names(self.request)
            return u'%s.%s.%s, %s:%s' % (date.day,
                                         local_months[date.month-1],
                                         date.year,
                                         '%02d' % (date.hour),
                                         '%02d' % (date.minute))
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
        local_months = localdatetime.get_month_names(self.request)
        for occurrence in self.version.get_occurrences():
            timezone = occurrence.get_timezone()
            location = occurrence.get_location()
            display_time = not occurrence.is_all_day()

            start = occurrence.get_start_datetime(timezone)
            end = occurrence.get_end_datetime(timezone)
            rec_til = occurrence.get_end_recurrence_datetime()

            start_str = u'%s.%s.%s' % (start.day,
                                       local_months[start.month-1],
                                       start.year)

            end_str = u'%s.%s.%s' % (end.day,
                                     local_months[end.month-1],
                                     end.year)

            if display_time:
                start_str = u'%s, %s:%s' % (start_str,
                                            '%02d' % (start.hour),
                                            '%02d' % (start.minute))
                end_str = u'%s, %s:%s' % (end_str,
                                          '%02d' % (end.hour),
                                          '%02d' % (end.minute))

            odi = {
                'start': start_str,
                'end': end_str,
                'location': location,
                'recurrence_until': rec_til,
            }

            if rec_til:
                rec_til_str = u'%s.%s.%s' % (rec_til.day,
                                             local_months[rec_til.month-1],
                                             rec_til.year)

                if display_time:
                    rec_til_str = u'%s, %s:%s' % (rec_til_str,
                                                  '%02d' % (rec_til.hour),
                                                  '%02d' % (rec_til.minute))

                odi['recurrence_until'] = rec_til_str
                recurrence = RRuleData(occurrence.get_recurrence()).get('FREQ')
                odi['recurrence'] = recurrence

            yield odi


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
