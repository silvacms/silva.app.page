##parameters=extsource
from Products.Silva.i18n import translate as _
model = context.REQUEST.model
view = context

if not extsource:
    return view.tab_edit(message_type='error', message=_("An external source must be selected."))
model.get_editable().set_part_name(extsource)
model.sec_update_last_author_info()

return view.tab_edit(message_type='feedback', message=_("External source name changed."))

