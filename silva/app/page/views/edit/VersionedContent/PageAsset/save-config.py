##parameters=extsource
from Products.Silva.i18n import translate as _
model = context.REQUEST.model
view = context

from Products.Formulator.Errors import ValidationError, FormValidationError

try:
    model.restrictedTraverse(['@@editview']).save_external_source_settings()
except FormValidationError, e:
    return context.tab_edit(message_type="error",
                            message=context.render_form_errors(e))
    

model.sec_update_last_author_info()

return view.tab_edit(message_type='feedback', message=_("External source properties saved."))

