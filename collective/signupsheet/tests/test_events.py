# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from uwosh.pfg.d2c.events import FormSaveData2ContentEntryFinalizedEvent
from zope.event import notify

from collective.signupsheet.tests.base import FunctionalTestCase


class TestEvents(FunctionalTestCase):
    """
    Test events configuration
    """

    def afterSetUp(self):
        FunctionalTestCase.afterSetUp(self)
        self.pwf = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Manager', ])
        self.create = self.portal.invokeFactory
        self.newid = self.create(type_name='SignupSheet', id='a-new-form')
        self.form = getattr(self.portal, self.newid)
        self.form.registrants.invokeFactory('registrant', id='rgs1')
        self.registrant = self.form.registrants['rgs1']

    def test_new_registrant(self):
        """
        Just to test that after notify the event, we have new state and a status
        setted
        """
        state = self.pwf.getInfoFor(self.registrant, 'review_state')
        self.assertTrue(state == 'new')
        self.assertTrue(self.registrant.ssfg_status == '')
        notify(FormSaveData2ContentEntryFinalizedEvent(self.registrant,
                                                       self.form))
        state = self.pwf.getInfoFor(self.registrant, 'review_state')
        self.assertTrue(state == 'unconfirmed')
        self.assertTrue(self.registrant.ssfg_status == 'registered')
