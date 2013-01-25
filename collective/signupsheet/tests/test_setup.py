# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from collective.signupsheet.tests.base import FunctionalTestCase

SSTYPE = 'SignupSheet'
REGISTRNAT = 'registrant'


class TestSetup(FunctionalTestCase):
    """
    Test setup configuration
    """

    def test_ss_in_portal_types(self):
        types = getToolByName(self.portal, 'portal_types')
        self.assertTrue(SSTYPE in types.objectIds())
        SS = types[SSTYPE]
        self.assertTrue('FormSaveData2ContentAdapter' in
                          tuple(SS.allowed_content_types))

    def test_portal_calendar(self):
        pcal = getToolByName(self.portal, 'portal_calendar')
        self.assertTrue(SSTYPE in pcal.calendar_types)
        self.assertTrue('open' in pcal.calendar_states)
        self.assertTrue('closed' in pcal.calendar_states)

    def test_registrant_in_portal_types(self):
        types = getToolByName(self.portal, 'portal_types')
        self.assertTrue(REGISTRNAT in types.objectIds())

    def test_properties(self):
        ptool = getToolByName(self.portal, 'portal_properties')
        site_prop = ptool.site_properties
        navtree_prop = ptool.navtree_properties
        self.assertTrue(SSTYPE in site_prop.default_page_types)
        self.assertTrue(REGISTRNAT in site_prop.types_not_searched)
        self.assertTrue(REGISTRNAT in navtree_prop.metaTypesNotToList)

    def test_tiny(self):
        tiny = getToolByName(self.portal, 'portal_tinymce')
        self.assertTrue(SSTYPE in tiny.linkable.split('\n'))
