import re

from silva.core.contentlayout.parts import ExternalSourcePart
from Products.Silva.testing import smi_settings
from PageTestCase import PageTestCase
from layer import FunctionalPageLayer


class ContentLayoutFunctionalTest(PageTestCase):
    
    layer = FunctionalPageLayer
    
    def setUp(self):
        super(ContentLayoutFunctionalTest, self).setUp()
        #copy an external source into the root
        self.login('manager')
        token = self.root.service_codesources.manage_copyObjects(["cs_toc",
                                                                  "cs_rich_text"])
        self.root.manage_pasteObjects(token)
        self.login('chiefeditor') 
        self.cs_name = "cs_toc"
        self.pageurl = '/root/page/'
        self.onetem = 'silva.core.contentlayout.templates.OneColumn'
        self.twotem = 'silva.core.contentlayout.templates.TwoColumn'
        
    def test_switch_template(self):
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = False

        #first switch the template
        sb.open(self.pageurl + '0/edit/switchlayouttemplate', 
                query={'newTemplate':self.twotem})
       
        #Make sure the default templates are in the drop down  
        sb.open(self.pageurl + 'edit')
        
        p = re.compile('<a class="yuimenuitemlabel"\n\s*value="(silva.*)">\n\s*<span class="template-name">(.*)</span>')
        
        s = p.search(sb.contents)
        
        # The page is using silva.contentlayouttempaltes.twocolum right now, so .onecolumn should be in the drop down
        self.assertEquals(self.onetem, s.group(1))
        self.assertEquals('One Column (standard)', s.group(2))
        
        #Switch to the other template do the same
        status = sb.open(self.pageurl + '0/edit/switchlayouttemplate', 
                         query={'newTemplate':self.onetem})
        sb.open(self.pageurl + 'edit')
        
        p = re.compile('<a class="yuimenuitemlabel"\n\s*value="(silva.*)">\n\s*<span class="template-name">(.*)</span>')
        
        s = p.search(sb.contents)

        # now the page is on .onecolumn, so .twocolumn should be in the drop down
        self.assertEquals(self.twotem, s.group(1))
        self.assertEquals('Two Column (standard)', s.group(2))
        
        status = sb.open(self.pageurl + '0/edit/switchlayouttemplate', 
                         query={'newTemplate':self.twotem})
        
    def test_parts(self):
        #Add an ES to the page
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True

        validation_url = self.pageurl + '0/edit/validateeditdialog'
        save_url = self.pageurl + '0/edit/savepart'
        switch_template = self.pageurl + '0/edit/switchlayouttemplate'

        #Test bad part type (i.e. non-existent codesource)
        status  = sb.open(validation_url, 
                          query={'parttype':'pe-title',
                                 'pagetitle':'Test'})
        self.assertEquals(500, status)

        #Change Page Title

        #Actually change it
        title_query = {'parttype':'page-title',
                              'pagetitle':'Test'}
        status = sb.open(validation_url, query=title_query)
        self.assertEquals(200, status)
        self.assertEquals('Success', sb.contents)
        
        status = sb.open(save_url, query=title_query)
        self.assertEquals(200, status)
        self.assertEquals('<h1 class="page-title">Test</h1>', sb.contents)

        #First, test validation
        status = sb.open(switch_template,
                         method='POST',
                         form={'newTemplate':
                               'silva.core.contentlayout.templates.TwoColumn'})
        self.assertEquals(status, 200)
        self.assertEquals('OK', sb.contents)

    def test_parts_validation(self):
        
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True

        validation_url = self.pageurl + '0/edit/validateeditdialog'
        save_url = self.pageurl + '0/edit/savepart'
        rich_copy = '<p>hi</p>'
        
        status = sb.open(validation_url, 
                         query={'parttype':'es',
                                'esname':'cs_rich_text',
                                'field_rich_text':rich_copy}
                         )
        self.assertEquals(200, status)
        self.assertEquals('Success', sb.contents)

        #Test invalid esname
        status = sb.open(validation_url,
                         query={'parttype':'es',
                                'esname':'cs_rich_tex',
                                'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing parttype
        status = sb.open(validation_url, 
                         query={'parttype':'',
                                'esname':'cs_rich_text',
                                'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing parttype
        status = sb.open(validation_url, 
                         query={'esname':'cs_rich_text',
                                'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing esname
        status = sb.open(validation_url, 
                         query={'parttype':'es',
                                'esname':'',
                                'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing esname
        status = sb.open(validation_url, 
                         query={'parttype':'es',
                                'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing field_rich_text
        status = sb.open(validation_url, 
                         query={'parttype':'es',
                                'esname':'cs_rich_text',
                                'field_rich_text':''}
                         )
        #unlike BadRequest, which is erroneously a 500/internal server error,
        # when formulator doesn't validate, a 400 is raised
        self.assertEquals(400, status)
        
        #Test missing field_rich_text
        status = sb.open(validation_url, 
                         query={'parttype':'es',
                                'esname':'cs_rich_text'}
                         )
        self.assertEquals(400, status)
        
    def test_parts_add_bad(self):
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True

        add_url = self.pageurl + '0/edit/addparttoslot'
        rich_copy = '<p>hi</p>'
        
        #Test invalid esname
        status = sb.open(add_url,
                         form={'parttype':'es',
                               'slotname':'feature',
                               'esname':'cs_bad',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing slotname
        status = sb.open(add_url, 
                         form={'parttype':'es',
                               'slotname':'',
                               'esname':'cs_rich_text',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing slotname
        status = sb.open(add_url, 
                         form={'parttype':'es',
                               'esname':'cs_rich_text',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing esname
        status = sb.open(add_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'esname':'',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing esname
        status = sb.open(add_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing field_rich_text
        status = sb.open(add_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'esname':'cs_rich_text',
                               'field_rich_text':''}
                         )
        self.assertEquals(500, status)
        
        #Test missing field_rich_text
        status = sb.open(add_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'esname':'cs_rich_text'}
                         )
        self.assertEquals(500, status)

    def test_parts_save(self):
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True

        add_url = self.pageurl + '0/edit/addparttoslot'
        save_url = self.pageurl + '0/edit/savepart'
        rich_copy = '<p>hi</p>'
        
        #actually add a part
        status = sb.open(add_url,
                         form={
                             'parttype':'es',
                             'slotname':'feature',
                             'esname':'cs_rich_text',
                             'field_rich_text':rich_copy}
                         )
        self.assertEquals(200, status)
        
        #We need to grab the partkey for later use
        divid = sb.html.xpath('//div[@class="part"]')[0].get('id')
        self.partkey = divid[divid.rfind('_')+1:]
        
        #Third, edit it
        status = sb.open(save_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'partkey':self.partkey,
                               'esname':'cs_rich_text',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(200, status)
        self.assertEquals(rich_copy, sb.contents)
        
        #Test invalid partkey
        status = sb.open(save_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'partkey':'0123456789',
                               'esname':'cs_rich_text',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        
        #Test missing partkey
        status = sb.open(save_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'partkey':'',
                               'esname':'cs_rich_text',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)
        #Test missing partkey

        status = sb.open(save_url, 
                         form={'parttype':'es',
                               'slotname':'feature',
                               'esname':'cs_rich_text',
                               'field_rich_text':rich_copy}
                         )
        self.assertEquals(500, status)

    def test_parts_move(self):
        #add a part, then move it
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True

        add_url = self.pageurl + '0/edit/addparttoslot'
        save_url = self.pageurl + '0/edit/savepart'
        move_url = self.pageurl + '0/edit/moveparttoslot'
        rich_copy = '<p>hi</p>'
        
        #first switch the template to two-column template
        status = sb.open(self.pageurl + '0/edit/switchlayouttemplate', 
                query={'newTemplate':self.twotem})
        self.assertEquals(200, status)

        #actually add a part
        status = sb.open(add_url,
                         form={
                             'parttype':'es',
                             'slotname':'feature',
                             'esname':'cs_rich_text',
                             'field_rich_text':rich_copy}
                         )
        self.assertEquals(200, status)
        
        #We need to grab the partkey for later use
        divid = sb.html.xpath('//div[@class="part"]')[0].get('id')
        self.partkey = divid[divid.rfind('_')+1:]

        #Test invalid partkey
        status = sb.open(move_url, 
                         form={'partkey':'123456',
                               'slotname':'panel'}
                         )
        self.assertEquals(500, status)
        
        #Test missing partkey
        status = sb.open(move_url,
                         form={'slotname':'panel',
                               'partkey':''}
                         )
        self.assertEquals(500, status)
        
        #Test missing partkey
        status = sb.open(move_url,
                         form={'slotname':'panel'}
                         )
        self.assertEquals(500, status)
        
        #Test missing slotname
        status = sb.open(move_url,
                         form={'slotname':'',
                               'partkey':self.partkey}
                         )
        self.assertEquals(500, status)
        
        #Test missing slotname
        status = sb.open(move_url,
                         form={'partkey':self.partkey}
                         )
        self.assertEquals(500, status)
        
        #Actually move it
        status = sb.open(move_url,
                         form={'partkey': self.partkey,
                               'slotname':'panel'}
                         )
        self.assertEquals(200, status)
        self.assertEquals('OK', sb.contents)

    def test_part_delete(self):
        #add a part, delete it
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True

        add_url = self.pageurl + '0/edit/addparttoslot'
        save_url = self.pageurl + '0/edit/savepart'
        move_url = self.pageurl + '0/edit/moveparttoslot'
        remove_url = self.pageurl + '0/edit/removepart'
        rich_copy = '<p>hi</p>'

        #Next, delete it
        
        #Test invalid partkey
        status = sb.open(remove_url, 
                         form={'partkey':'0123456789'}
                         )
        self.assertEquals(500, status)
        
        #Test missing partkey
        status = sb.open(remove_url, 
                         form={'partkey':''}
                         )
        self.assertEquals(500, status)
        
        #Test missing partkey
        status = sb.open(remove_url)
        self.assertEquals(500, status)

        #Actually delete it (add it first)
        status = sb.open(add_url,
                         form={
                             'parttype':'es',
                             'slotname':'feature',
                             'esname':'cs_rich_text',
                             'field_rich_text':rich_copy}
                         )
        self.assertEquals(200, status)
        
        #Grab the key
        #We need to grab the partkey for later use
        divid = sb.html.xpath('//div[@class="part"]')[0].get('id')
        self.partkey = int(divid[divid.rfind('_')+1:])
        
        status = sb.open(remove_url, 
                         form={'partkey': self.partkey}
                         )
        self.assertEquals(200, status)
        self.assertEquals('OK', sb.contents)

    def test_part_move_multiple(self):
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True

        add_url = self.pageurl + '0/edit/addparttoslot'
        save_url = self.pageurl + '0/edit/savepart'
        move_url = self.pageurl + '0/edit/moveparttoslot'
        remove_url = self.pageurl + '0/edit/removepart'
        rich_copy = '<p>hi</p>'
        editable = self.page.get_editable()

        #Finally, test with more than one part

        #part one (in feature slot)
        status = sb.open(add_url,
                         form={
                             'parttype':'es',
                             'slotname':'feature',
                             'esname':'cs_rich_text',
                             'field_rich_text':rich_copy}
                         )
        self.assertEquals(200, status)
        
        #Grab the key
        #We need to grab the partkey for later use
        divid = sb.html.xpath('//div[@class="part"]')[0].get('id')
        self.partkey1 = int(divid[divid.rfind('_')+1:])

        #part two (in panel slot)
        status = sb.open(add_url,
                         form={
                             'parttype':'es',
                             'slotname':'panel',
                             'esname':'cs_rich_text',
                             'field_rich_text':rich_copy}
                         )
        self.assertEquals(200, status)
        
        #Grab the key
        #We need to grab the partkey for later use
        divid = sb.html.xpath('//div[@class="part"]')[0].get('id')
        self.partkey2 = int(divid[divid.rfind('_')+1:])

        #Move part one to the same slot as part two (i.e. panel)
        status = sb.open(move_url, 
                         form={'partkey': self.partkey1,
                                    'slotname':'panel'}
                              )
        self.assertEquals(200, status)
        self.assertEquals('OK', sb.contents)
        #verify order
        parts = [ p.get_key() for p in editable.get_parts_for_slot('panel') ]
        self.assertEquals(parts, [self.partkey2, self.partkey1])
        

        #Move part one back to feature
        status = sb.open(move_url,
                         form={'partkey':self.partkey1,
                               'slotname':'feature'}
                         )
        self.assertEquals(200, status)
        self.assertEquals('OK', sb.contents)
        #verify order
        ps = [ p.get_key() for p in editable.get_parts_for_slot('feature') ]
        self.assertEquals(ps, [self.partkey1])

        #Move part two to feature, put it before part1
        status = sb.open(move_url, 
                         form={'partkey':self.partkey2,
                               'slotname':'feature',
                               'beforepartkey':self.partkey1}
                         )
        self.assertEquals(200, status)
        self.assertEquals('OK', sb.contents)
        #verify order
        ps = [ p.get_key() for p in editable.get_parts_for_slot('feature') ]
        self.assertEquals(ps, [self.partkey2, self.partkey1])

    def test_addSilvaPage(self):
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = False
        sb.open('/root/edit/tab_edit')
        
        #ensure silva page is in the add list
        af = sb.get_form(name="md.container")
        content = af.get_control('md.container.field.content')
        self.failUnless('Silva Page' in content.options)

        #set value for add form, submit
        content.value = 'Silva Page'
        status = af.submit('md.container.action.new')
        self.assertEquals(status, 200)
        self.assertEquals(sb.location, '/root/edit/+/Silva Page')

        #specify values for new content, submit
        addform = sb.get_form('addform')
        addform.controls['addform.field.title'].value = 'page 2'
        addform.controls['addform.field.id'].value = 'page2'
        addform.controls['addform.field.template'].value = \
               'silva.core.contentlayout.templates.OneColumn'
        status = addform.submit('addform.action.save_edit')
        self.assertEquals(status, 200)
        self.assertEquals(sb.location, '/root/page2/edit')
        
    def test_addSilvaPageAsset(self): 
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = False
        sb.open('/root/edit/tab_edit')

        #ensure silva page is in the add list
        af = sb.get_form(name="md.container")
        content = af.get_control('md.container.field.content')
        self.failUnless('Silva Page Asset' in content.options)

        #set value for add form, submit
        content.value = 'Silva Page Asset'
        status = af.submit('md.container.action.new')
        self.assertEquals(status, 200)
        self.assertEquals(sb.location, '/root/edit/+/Silva Page Asset')

        addform = sb.get_form('addform')
        addform.controls['addform.field.title'].value = 'pa2'
        addform.controls['addform.field.id'].value = 'pa2'
        addform.controls['addform.field.part_name'].value = 'cs_rich_text'
        status = addform.submit('addform.action.save_edit')
        self.assertEquals(status, 200)
        self.assertEquals(sb.location, '/root/pa2/edit')
        
    def test_pageAssetEditActions(self):
        sb = self.layer.get_browser(smi_settings)
        sb.login('editor')
        sb.options.handle_errors = True
        url = '/root/pageasset/edit/'
        
        #Empty extsource name
        status = sb.open(url,
                        method='POST',
                        form={'extsource':'',
                              'change-es:method':'change externalsource'})
        sb.inspect.add('alert', "//div[@class='fixed-alert']")
        self.assertEquals(sb.inspect.alert, 
                          ['An external source must be selected.'])

        #Now actually add it
        status = sb.open(url, 
                         method='POST',
                         form={'extsource':'cs_rich_text',
                               'change-es:method':'change external source'}
                         )
        control = sb.get_form('silvaObjects').get_control('esname')
        self.assertEquals(control.value, 'cs_rich_text')


import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContentLayoutFunctionalTest))
    return suite
