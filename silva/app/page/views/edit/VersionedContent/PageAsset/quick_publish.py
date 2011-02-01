from Products.Silva.i18n import translate as _
model = context.REQUEST.model
view = context

#get the tab to return to, defaulting to tab_edit
return_to_id = context.REQUEST.get('return_to', 'tab_edit')
return_to = getattr(view, return_to_id, None)
if return_to is None:
    return_to = getattr(view, 'tab_edit')

if not model.get_unapproved_version():
    # SHORTCUT: To allow approval of closed docs with no new version available,
    # first create a new version. This "shortcuts" the workflow.
    # See also edit/Container/tab_status_approve.py
    if model.is_version_published():
        return return_to(
            message_type="error", 
            message=_("There is no unapproved version to approve."))
    model.create_copy()   
    
if not getattr(model, model.get_unapproved_version()).getName():
    return return_to(
        message_type="error", 
        message=_("An external source must be selected."))

import DateTime

model.set_unapproved_version_publication_datetime(DateTime.DateTime())

model.approve_version()

if hasattr(model, 'service_messages'):
    model.service_messages.send_pending_messages()


return return_to(message_type="feedback", message=_("Version approved."))
