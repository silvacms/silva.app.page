
from five import grok
from grokcore.chameleon.components import ChameleonPageTemplate
from zope.cachedescriptors.property import CachedProperty
from zope.component import getUtility, getMultiAdapter
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.browser import absoluteURL

from silva.app.news.interfaces import IServiceNews
from silva.core.contentlayout.blocks import Block, BlockController
from silva.core.contentlayout.interfaces import IBlockController, IBlockManager
from silva.translations import translate as _
from silva.ui.rest import UIREST

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

    def render(self):
        return self.template.render(self)


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

    message = _(u'Block created.')
    autoclose = 4000

    def __init__(self, context, request, restriction=None):
        super(AddBlockREST, self).__init__(context, request)
        self.restriction = restriction

    def _create_block(self):
        raise NotImplementedError

    def POST(self):
        block = self._create_block()
        block_id = IBlockManager(self.context).add(
            self.__parent__.slot_id, block)
        controller = getMultiAdapter(
            (block, self.context, self.request), IBlockController)
        notify(ObjectModifiedEvent(self.context))

        return self.json_response(
            {'content' :
                 {'extra':
                      {'block_id': block_id,
                       'block_data': controller.render(),
                       'block_editable': False},
                  'success': True},
             "notifications": [{"category": "",
                                "message": self.message,
                                "autoclose": self.autoclose}],
             })


class AddNewsBlockREST(AddBlockREST):
    grok.adapts(NewsInfoBlock, INewsPageVersion)

    message = _(u'News info block added.')

    def _create_block(self):
        return NewsInfoBlock()


class AddAgendaBlockREST(AddBlockREST):
    grok.adapts(AgendaInfoBlock, IAgendaPageVersion)

    message = _(u'Agenda info block added.')

    def _create_block(self):
        return AgendaInfoBlock()
