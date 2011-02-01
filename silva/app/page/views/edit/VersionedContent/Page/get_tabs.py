## Script (Python) "get_tabs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# dev note: somewhere - maybe here - we should read the user's
# editor preferences and serve the appropriate tab_edit template
#
# define:
# name, id, up_id, toplink_accesskey, tab_accesskey, uplink_accesskey
from Products.SilvaDocument.i18n import translate as _

tabs = [(_('editor'), 'tab_edit', 'tab_edit', '!', '1', '6'),
        (_('properties'), 'tab_metadata', 'tab_metadata', '@', '2', '7'),
        (_('access'), 'tab_access', 'tab_access', '#', '3', '8'),
        (_('publish'), 'tab_status', 'tab_status', '$', '4', '9'),
       ]

return tabs
