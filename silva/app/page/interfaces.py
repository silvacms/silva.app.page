from silva.core.interfaces import (ICatalogedVersionedAsset, IVersion,
                                   ICatalogedVersionedContent)
from silva.core.contentlayout.interfaces import (IVersionedContentLayout,
                                                 IContentLayout)

class IPage(ICatalogedVersionedContent, IVersionedContentLayout):
    pass

class IPageVersion(IVersion, IContentLayout):
    pass

class IPageAsset(ICatalogedVersionedAsset):
    pass

class IPageAssetVersion(IVersion):
    pass
