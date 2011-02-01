## Script (Python) "tab_preview"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=message_type=None,message=None
##title=
##

model = context.REQUEST.model

#Silva Pages do not have preview tabs.  Redirect to the edit screen
# if accessed.
context.REQUEST.RESPONSE.redirect(model.absolute_url() + '/edit/tab_edit')
return

