from silva.core.interfaces import (IVersionedAsset, IVersion,
                                   IVersionedContent)
from silva.core.contentlayout.interfaces import (IVersionedContentLayout,
                                                 IContentLayout)

class IPage(IVersionedContent, IVersionedContentLayout):
    """ A Silva Page represents a web page, supporting advanced
        inline editing and content layout.
    """

class IPageVersion(IVersion, IContentLayout):
   """A version of a Silva Page (i.e. a web page) """
 
class IPageAsset(IVersionedAsset):
    """A Page Asset is a versioned instance of an External
       Source, which can be placed/reused on multiple Silva Pages.
    """

class IPageAssetVersion(IVersion):
    """A version of a Page Asset
    """

    def set_part_name(name):
        """set the name of the external source 'part' used by this
           page asset.  Will reinitialize the config
        """
        
    def get_part_name():
        """returns the external source 'part' used by this page asset
        """
        
    def set_config(config_dict):
        """stores the config dictionary for this page asset's
           external source
        """
        
    def get_config():
        """returns a copy of the config dictionary for this page asset.
        """