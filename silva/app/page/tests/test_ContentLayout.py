from zExceptions import NotFound
from zope.component.interfaces import ComponentLookupError

from silva.core.contentlayout.parts import ExternalSourcePart
from silva.core.contentlayout.interfaces import IPartFactory

from PageTestCase import PageTestCase

class ContentLayoutClassTestCase(PageTestCase):
    #this is really test_Page (since ContentLayout is a base class)
    
    def setUp(self):
        super(ContentLayoutClassTestCase, self).setUp()
        self.layoutName = 'silva.core.contentlayout.templates.TwoColumn'
      
        #copy an external source into the root
        #self.installExtension("SilvaExternalSources")
        self.login('manager')
        token = self.root.service_codesources.manage_copyObjects(["cs_toc"])
        self.root.manage_pasteObjects(token)
        self.login('chiefeditor')
        
    def test_LayoutName(self):
        
        # test to make sure switching template works
        e = self.page.get_editable()
        e.switch_template(self.layoutName)
        self.assertEquals(self.layoutName, e.get_layout_name())
        #Test to make sure invalid template name raises error
        self.assertRaises(ComponentLookupError, e.switch_template, ';lkasj')
        
    def test_SlotName(self):
        
        e = self.page.get_editable()
        e.switch_template(self.layoutName)
        #Make sure the slot name initially does not exist
        self.assertEquals(None, e.get_slot('feature', False))
        #Confirm slot is created empty
        self.assertEquals([], e.get_slot('feature', True))

    def test_addPartToSlot(self):
        e = self.page.get_editable()
        cs = getattr(self.root, 'cs_toc')
        factory = IPartFactory(cs)
        part = factory.create({'paths':'pub'})
        self.assertRaises(TypeError, e.add_part_to_slot, part, None)

    def test_PartsForSlot(self):
        e = self.page.get_editable()
        e.switch_template(self.layoutName)
        e.get_slot('feature', True)
        #Make sure there are no parts in slot
        self.assertEquals(0, len(list(e.get_parts_for_slot('feature'))))
        
        cs = getattr(self.root, 'cs_toc')
        factory = IPartFactory(cs)
        part = factory.create({'paths':'pub'})
        part2 = factory.create({'paths':'pub2'})
        e.add_part_to_slot(part, 'feature')
        #Make sure there is only one part  slot
        self.assertEquals(1, len(list(e.get_parts_for_slot('feature'))))
        e.remove_part(part.get_key())
        #Make sure part was removed properly
        self.assertEquals(0, len(list(e.get_parts_for_slot('feature'))))
        #Make sure removing a part not in slot fails
        self.assertRaises(KeyError, e.remove_part,part.get_key())

        e.add_part_to_slot(part, 'feature')
        e.move_part_to_slot(part.get_key(), 'left')
        #Make sure moving parts between slots works
        self.assertEquals(0, len(list(e.get_parts_for_slot('feature'))))
        self.assertEquals(1, len(list(e.get_parts_for_slot('left'))))
        
        #Make sure that trying to add duplicate part doesn't work
        self.assertRaises(TypeError, e.add_part_to_slot, part, 'feature')
       
        e.remove_part(part.get_key())
        e.add_part_to_slot(part, 'feature')
        e.add_part_to_slot(part2, 'feature')
        #Make sure we can add multiple parts to slot
        self.assertEquals(2, len(list(e.get_parts_for_slot('feature'))))
        
    def test_getParts(self):
        e = self.page.get_editable()
        e.switch_template(self.layoutName)
        e.get_slot('feature', True)
        #Make sure there are no parts in slot
        self.assertEquals(0, len(list(e.get_parts_for_slot('feature'))))
        cs = getattr(self.root, 'cs_toc')
        factory = IPartFactory(cs)
        part = factory.create({'paths':'pub'})
        part2 = factory.create({'paths':'pub2'})
        e.add_part_to_slot(part, 'feature')
        e.add_part_to_slot(part2, 'panel' )
        
        self.assertEquals(2, len(list(e.get_parts())))
        self.assertRaises(TypeError, 3, len(list(e.get_parts())))
        
    def test_slotNameForPart(self):
        e = self.page.get_editable()
        e.switch_template(self.layoutName)
        e.get_slot('feature', True)
       
        cs = getattr(self.root, 'cs_toc')
        factory = IPartFactory(cs)
        part = factory.create({'paths':'pub'})
        
        e.add_part_to_slot(part, 'feature')
        #Make sure we can get correct slot a part is in
        self.assertEquals('feature', e.get_slot_name_for_part(part))
        #Make sure that proper error is raised if a part is not specified
        self.assertRaises(AttributeError, e.get_slot_name_for_part, None)

    def test_SwitchTemplate(self):
        e = self.page.get_editable()
        e.switch_template(self.layoutName)
        self.assertEquals(self.layoutName, e.get_layout_name())
        #Test to see if we can switch to same template
        e.switch_template(self.layoutName)
        self.assertEquals(self.layoutName, e.get_layout_name())
        
        cs = getattr(self.root, 'cs_toc')
        factory = IPartFactory(cs)
        part = factory.create({'paths':'pub'})
        part2 = factory.create({'paths':'pub2'})
        e.add_part_to_slot(part, 'panel')
        e.add_part_to_slot(part2, 'panel')
        
        #Switch templates multiple times to make sure parts move properly
        e.switch_template('silva.core.contentlayout.templates.OneColumn')
        e.switch_template('silva.core.contentlayout.templates.TwoColumn')
        e.switch_template('silva.core.contentlayout.templates.OneColumn')
        e.switch_template('silva.core.contentlayout.templates.TwoColumn')
        self.assertEquals('silva.core.contentlayout.templates.TwoColumn',
                          e.get_layout_name())
        # test to make sure the parts are in the correct slot
        self.assertEquals(2, len(list(e.get_parts_for_slot('feature'))))

import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ContentLayoutClassTestCase))
    return suite
