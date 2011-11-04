
from silva.core.interfaces import IVersion,  IVersionedContent
from silva.core.contentlayout.interfaces import IPage as IBasicPage


class IPage(IVersionedContent, IBasicPage):
    """ A web page.

    This content supports advanced inline editing and content layout.
    """


class IPageVersion(IVersion):
   """A version of a Silva Page (i.e. a web page)
   """

