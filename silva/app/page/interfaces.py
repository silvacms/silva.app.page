
from silva.core.interfaces import IVersion,  IVersionedContent
from silva.core.contentlayout.interfaces import IPage as IBasicPage
from silva.core.contentlayout.interfaces import IPageAware


class IPage(IVersionedContent, IPageAware):
    """ A web page.

    This content supports advanced inline editing and content layout.
    """


class IPageVersion(IVersion, IBasicPage):
   """A version of a Silva Page (i.e. a web page)
   """

