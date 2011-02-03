
from logging import getLogger
logger = getLogger('silva.app.page.pageasset')

# Zope 3
from five import grok
from zope.interface import Interface, alsoProvides
from zope.component import getMultiAdapter, queryMultiAdapter
from zope.app.container.interfaces import IObjectRemovedEvent
from persistent.mapping import PersistentMapping
from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from megrok import pagetemplate as pt

# Zope 2
from zExceptions import BadRequest
from OFS import Folder
from OFS.interfaces import IObjectWillBeAddedEvent
from AccessControl import ClassSecurityInfo, getSecurityManager
from App.class_init import InitializeClass
from Acquisition import aq_inner

from Products.Formulator.Errors import FormValidationError
from Products.Silva import SilvaPermissions
from Products.Silva.VersionedAsset import VersionedAsset
from Products.Silva.Version import Version
from Products.SilvaExternalSources.interfaces import IExternalSource
from Products.SilvaExternalSources import ExternalSource
from silva.translations import translate as _
from silva.core import conf as silvaconf
from silva.core.smi.interfaces import IEditTabIndex
from zeam.form import silva as silvaforms
from zeam.form import base
from zeam.form.base.markers import NO_VALUE, SUCCESS, FAILURE, DISPLAY

from silva.core.contentlayout.interfaces import IPartFactory, IPartEditWidget
from silva.app.page.interfaces import IPageAsset, IPageAssetVersion
#from browser.interfaces import IContentLayoutPartEditWidget


class PageAssetVersion(Version):
    """A version of a Page Asset"""
    
    security = ClassSecurityInfo()
    
    grok.implements(IPageAssetVersion)
    
    meta_type = "Silva Page Asset Version"

    def __init__(self, id):
        """Initialize PageAssetVersion"""
        
        PageAssetVersion.inheritedAttribute('__init__')(self, id)
        self._part = None

    def _get_source(self, esname):
        """private function to get the ExternalSource `esname`
           within the current context
        """
        
        try:
            source = getattr(self.aq_inner,esname)
        except AttributeError:
            raise BadRequest()
        if not IExternalSource.providedBy(source):
            raise BadRequest()
        return source
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'set_part_name')
    def set_part_name(self, name):
        #ensure source is accessible, this will raise an error if not
        source = self._get_source(name)
        pf = IPartFactory(source)
        #create a part associated with the source, with an empty config
        # (since we don't have a config yet)
        self._part = pf.create({})

    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'get_part_name')
    def get_part_name(self):
        if not self._part:
            return None
        return self._part.get_name()

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'set_config')
    def set_config(self, config_dict):
        #convert config to a dict, then create a PersistentMapping
        # out of it.  
        d = PersistentMapping(dict(config_dict))
        self._part.set_config(d)
        
    security.declareProtected(SilvaPermissions.AccessContentsInformation,
                              'get_config')
    def get_config(self):
        if not self._part:
            return None
        #always return a copy of the config, to prevent accidental modification.
        #  use set_config to update this object's config.
        return self._part.get_config(copy=True)

InitializeClass(PageAssetVersion)
    

class PageAsset(VersionedAsset):
    """A Page Asset is a versioned instance of an External
       Source, which can be placed/reused on multiple Silva Pages.
    """
    
    meta_type = "Silva Page Asset"
    
    security = ClassSecurityInfo()
    
    grok.implements(IPageAsset)
    silvaconf.icon("pageasset.png")
    silvaconf.versionClass(PageAssetVersion)
    
    def __init__(self, id):
        """Initialize PageAsset""" 
        PageAsset.inheritedAttribute('__init__')(self, id)
        
InitializeClass(PageAsset)

class PartEditViewHelper(grok.View):
    """This class exists to provide grok helper functions to the
       SilvaViews-based PageAsset edit tab.  The functionality provided
       by this class will be transitioned into the relevant grok views
       in Silva 2.4
    """
    grok.context(IPageAsset)
    grok.name('editview')
    grok.require('silva.ChangeSilvaContent')

    security = ClassSecurityInfo()
    
    def get_external_source_list(self):
        """Return an ordered list of the External Sources within the
           current context.  Each item is a three-tuple of 
           [ priority, title, name, source ]"""
        sources = [ [s[1].priority(), s[1].title.encode('utf-8'),s[0], s[1]] \
                    for s in ExternalSource.availableSources(aq_inner(self.context))
                    if s[1].id != 'cs_page_asset' ]
        sources.sort()
        return sources

    def get_edit_dialog(self):
        """Displays the edit dialog for the editable version's
           Part (an IPartEditWidget)"""
        editable = self.context.get_editable()
        source = editable._get_source(editable.get_part_name())
        ad = getMultiAdapter((source, self.request),
                             name='part-edit-widget')
        #reuse the ContentLayoutEditor's part edit widget.
        #this requires that some "dummy" info be passed in,
        # (this info is only added as hidden input fields
        # to the form)
        return ad(contentlayout=editable,
                  mode="edit",
                  slotname="a",
                  partkey=12345,
                  partconfig=editable.get_config(),
                  submitButtonName="save-config:method",
                  from_request=self.request.form.has_key('save-config'),
                  suppressFormTag=True,
                  submitOnTop=True)
    
    #this declaration is needed to support calling this from a PythonScript
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
                              'save_external_source_settings')
    def save_external_source_settings(self):
        """save the external source settings for the editable
           versions external source.
           Raises FormValidationError if the validation fails."""
        editable = self.context.get_editable()
        source = editable._get_source(editable.get_part_name())
        form = source.get_parameters_form()
        result = form.validate_all(self.request)
        editable.set_config(dict(result))
    
    def render(self):
        """there is no render for this, it's just a grok helper class.
           It's a view so it is easily accessible via path traversal in
           path expressions"""
        return u""
InitializeClass(PartEditViewHelper)

#-------------
# ADD VIEW
#-------------

@grok.provider(IContextSourceBinder)
def externalsources_source(context):
    """Return a SimpleVocabulary of the available external sources in
    the supplied context"""
    
    vocab = [SimpleTerm(value=None, token=None, title=u"Not Set")]
    sources = []
    for es in ExternalSource.availableSources(aq_inner(context)):
        if es[1].id != 'cs_page_asset':
            sources.append( [es[1].priority(), es[1].title.encode('utf-8'), 
                             unicode(es[1].id) ] )
    sources.sort()
    
    for s in sources:
        vocab.append(SimpleTerm(
            value=s[2],
            token=s[2],
            title=s[1]
            ))
    return SimpleVocabulary(vocab)

class IExternalSourceSchema(Interface):
    """Schema for listing the available external sources"""
    part_name = schema.Choice(
        title=_(u"External Source"),
        description=_(u"The external source for this Silva Page Asset"),
        source=externalsources_source,
        required=True)
    
class IPageAssetAddSchema(silvaconf.interfaces.IBasicTitledContent,
                          IExternalSourceSchema):
    """The schema for the page asset add screen is the
       id, title, and the asset's initial external source"""

class PageAssetAddView(silvaforms.SMIAddForm):
    """Simple Add form for a page asset"""
    grok.context(IPageAsset)
    grok.name(u'Silva Page Asset')
    
    fields = silvaforms.Fields(IPageAssetAddSchema)

    def _add(self, parent, data):
        """Overrides the default add handler so that the external source
           can also be set.
        """
        content = super(PageAssetAddView, self)._add(parent, data)
        name = data.getWithDefault('part_name')
        if name is not None:
            content.get_editable().set_part_name(name)
        return content

#-------------
# EDIT VIEW
# NOTE :: for 2.3 this is commented out.  When SMI edit screens are more
#         completely supported (in 2.4) this will be revisited
#-------------

#class IPageAssetResources(IDefaultBrowserLayer):
    #"""Adds custom css to the edit screen (applied in PageAssetEditView.update"""
    #silvaconf.resource('pa-edit-styles.css')

#class PageAssetEditView(silvaforms.SMIComposedEditForm):
    #"""Edit View for a page asset.  This form is composed of
       #two sub-forms, the first enables switching the external source, the
       #second for editing the external source."""
    #grok.context(IPageAsset)

    #label = _(u"edit page asset")
    ##description = _(u"this screen lets you edit page assets")
    
    #def update(self):
        #alsoProvides(self.request, IPageAssetResources)
        #super(PageAssetEditView, self).update()
        #if self.mode == DISPLAY:
            #self.label = "Preview Page Asset"
            #self.updateWidgets()
            
    #def isDisplayMode(self):
        #return self.mode == DISPLAY

#class PageAssetEditViewTemplate(silvaforms.form.SMIComposedEditFormTemplate):
    #"""a custom composed edito form for page assets, to tie in a hackish
       #"published" view"""
    #pt.view(PageAssetEditView)
    

#class PAChangeAction(silvaforms.EditAction):
    #"""Action for the ChangeSource sub-form"""
    #title=_(u"Change External Source")

#class ChangeSource(silvaforms.SMISubForm):
    #"""Page Asset edit screen sub-form for switching external sources"""
    #grok.context(IPageAsset)
    #grok.order(1)
    #grok.view(PageAssetEditView)
    #label = _(u"Change External Source")
    #dataManager = silvaforms.form.SilvaDataManager
    #ignoreContent = False
    
    #fields = silvaforms.Fields(IExternalSourceSchema)
    #actions = base.Actions(PAChangeAction(),)

#class PAEditAction(silvaforms.EditAction):
    #"""`Save` action/button for the edit external source subform.
       #Attempts to get the source, validate the params and set the
       #params as the config on the Page Asset.
    #"""
    #title=_(u"Save")
    
    #def render_errors(self, errors):
        #"""format the validation errors returned by the external source's
           #validator"""
        #result = []
        #if len(errors.errors) == 1:
        
            #error = errors.errors[0]
            #error_text = error.error_text
            #title = error.field['title']
        
            ## translate error_text and title first
            #error_text = error_text
            #title = title
        
            #result.append('%s: %s' % (title, error_text))
            #return (''.join(result))
        
        #else:
        
            #for error in errors.errors:
                #error_text = error.error_text
                #title = error.field['title']
            
                ## translate error_text and title first
                #error_text = error_text
                #title = title
            
                #result.append('<li class="error">%s: %s</li>\n' %  (title, error_text))
        
        #return ("""<dl style="margin:0;"><dt>""" + \
                #"Sorry, there are problems with these form fields:" + \
                #"""</dt><dd><ul class="tips">""" + \
                #' '.join(result) + \
                #"</ul></dd></dl>")

    #def __call__(self, form):
        #"""save the external source settings for the editable
           #versions external source."""
        #editable = form.context.get_editable()
        #source = editable._getSource(editable.get_part_name())
        #esform = source.get_parameters_form()
        #try:
            #result = esform.validate_all(form.request)
            #editable.setConfig(dict(result))
            #form.send_message(_(u"Changes saved."), type="feedback")
            #return SUCCESS
        #except FormValidationError, err:
            #errors = self.render_errors(err)
            #form.send_message(errors, type="error")
            #return FAILURE

#class EditExternalSource(silvaforms.SMISubForm):
    #"""Page Asset sub-form for editing it's external source settings"""
    #grok.context(IPageAsset)
    #grok.order(10)
    #grok.view(PageAssetEditView)
    #label = _(u"Edit External Source")
    
    #actions = base.Actions(PAEditAction(),)
    
    #def __init__(self, *args, **kw):
        #super(EditExternalSource, self).__init__(*args, **kw)
        
    #def update(self):
        #"""pre-compute the editable version and the name of 
           #external source, if available."""
        #self.editable = self.context.get_editable()
        #self.name = None
        #if self.editable:
            #self.name = self.editable.get_part_name()
        #super(EditExternalSource, self).update()
   
            
    #def editDialog(self):
        #"""Displays the edit dialog for the editable version's
           #Part (an IPartEditWidget)"""
        #if not (self.editable and self.name):
            ##if no source defined yet (perhaps pageasset was just created)
            ## or source is not editable, do not display edit dialog
            #return u""
        #source = self.editable._getSource(self.name)
        #ad = getMultiAdapter((source, self.request),
                             #name='part-edit-widget')
        ##reuse the ContentLayoutEditor's part edit widget.
        ##this requires that some "dummy" info be passed in,
        ## (this info is only added as hidden input fields
        ## to the form)
        #return ad(contentlayout=self.editable,
                  #mode="edit",
                  #slotname="a",
                  #partkey=12345,
                  #partconfig=self.editable.getConfig(),
                  #submitButtonName="form.editexternalsource.action.save",
                  #from_request=self.request.form.has_key('save-config'),
                  #suppressFormTag=True,
                  #submitOnTop=True)
    
#class EditExternalSourceTemplate(silvaforms.form.SMISubFormTemplate):
    #"""override the subform template for the external source edit subform"""
    #grok.view(EditExternalSource)
