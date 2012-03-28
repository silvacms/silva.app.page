
from five import grok
from grokcore.chameleon.components import ChameleonPageTemplate
from zope.cachedescriptors.property import CachedProperty
from zope.component import getUtility
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.browser import absoluteURL

from silva.app.news.interfaces import IServiceNews
from silva.core.contentlayout.blocks import Block
from silva.core.contentlayout.interfaces import IBlockController
from silva.translations import translate as _

from .interfaces import INewsPageVersion, IAgendaPageVersion


class NewsInfoBlock(Block):
    grok.context(INewsPageVersion)
    grok.name('news-info')
    grok.title(_(u'News info'))
    grok.order(50)


class AgendaInfoBlock(Block):
    grok.context(IAgendaPageVersion)
    grok.name('agenda-info')
    grok.title(_(u'Agenda info'))
    grok.order(50)


class NewsInfoBlockController(grok.MultiAdapter):
    grok.adapts(NewsInfoBlock, INewsPageVersion, IHTTPRequest)
    grok.provides(IBlockController)

    template = ChameleonPageTemplate(filename="templates/newsinfo.cpt")

    def __init__(self, block, version, request):
        self.version = version
        self.request = request

    def remove(self):
        pass

    @CachedProperty
    def url(self):
        return absoluteURL(self.version.get_content(), self.request)

    @CachedProperty
    def format_date(self):
        return getUtility(IServiceNews).format_date

    @CachedProperty
    def publication_date(self):
        date = self.context.get_display_datetime()
        if date:
            return self.format_date(date)
        return u''

    def default_namespace(self):
        return {}

    def namespace(self):
        return {'version': self.version,
                'request': self.request,
                'view': self}

    def render(self):
        return self.template.render(self)


class AgendaInfoBlockControl(NewsInfoBlockController):
    grok.adapts(NewsInfoBlock, IAgendaPageVersion, IHTTPRequest)

    template = ChameleonPageTemplate(filename="templates/agendainfo.cpt")

    def occurrences(self):
        for occurrence in self.version.get_occurrences():
            timezone = occurrence.get_timezone()
            yield {
                'start': self.format_data(
                    occurrence.get_start_datetime(timezone),
                    occurrence.is_all_day()),
                'end': self.format_date(
                    occurrence.get_end_datetime(timezone),
                    occurrence.is_all_day()),
                'location': occurrence.get_location()}
