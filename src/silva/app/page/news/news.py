
from five import grok

from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass

from Products.Silva.VersionedContent import VersionedContent
from Products.Silva.Version import Version

from silva.core import conf as silvaconf
from silva.app.news.NewsItem import NewsItemContent
from silva.app.news.NewsItem import NewsItemContentVersion
from silva.app.news.NewsItem import INewsItemSchema
from silva.core.contentlayout.interfaces import ITitledPage
from zeam.form import silva as silvaforms

from .interfaces import INewsPage, INewsPageVersion


class NewsPageVersion(NewsItemContentVersion, Version):
    security = ClassSecurityInfo()
    meta_type = 'Silva News Page Version'
    grok.implements(INewsPageVersion)


InitializeClass(NewsPageVersion)


class Page(NewsItemContent, VersionedContent):
    """ A Silva Page represents a web page, supporting advanced
        inline editing and content layout.
    """
    security = ClassSecurityInfo()
    grok.implements(INewsPage)
    meta_type = 'Silva News Page'
    silvaconf.icon('news/news.png')
    silvaconf.version_class(NewsPageVersion)
    silvaconf.priority(-9)


InitializeClass(Page)


class PageAddForm(silvaforms.SMIAddForm):
    """Add form for an agenda page.
    """
    grok.context(INewsPage)
    grok.name(u'Silva News Page')

    fields = silvaforms.Fields(ITitledPage, INewsItemSchema)
