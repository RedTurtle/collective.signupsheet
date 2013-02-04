# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

from uwosh.pfg.d2c.events import FormSaveData2ContentEntryFinalizedEvent
from zope.event import notify

from collective.signupsheet.tests.base import FunctionalTestCase


def onSuccessMock(fields, REQUEST):
    return True


class TestForm(FunctionalTestCase):
    """
    Use this test class to test SignupSheet form configuration
    """

    def afterSetUp(self):
        FunctionalTestCase.afterSetUp(self)
        self.setRoles(['Manager', ])
        self.pwf = getToolByName(self.portal, 'portal_workflow')
        self.create = self.portal.invokeFactory
        self.newid = self.create(type_name='SignupSheet', id='a-new-form')
        self.form = getattr(self.portal, self.newid)
        self.form.setEventsize(1)
        self.form.setEventsize(1)
        # need to mock onSuccess: we don't test mail
        self.form['user_notification_mailer'].onSuccess = onSuccessMock

    def test_available_action(self):
        """
        A new registrant could be 'redirected' in an unconfirmed state or in
        waitinglist_unconfirmed state. Check transitions
        """
        self.form.registrants.invokeFactory('registrant', id='rgs1')
        self.registrant = self.form.registrants['rgs1']
        transitions = [transition['id'] for transition in
                       self.pwf.listActionInfos(object=self.registrant)]
        self.assertTrue('post' in transitions)
        self.assertTrue('post_waitinglist' in transitions)

    def test_registrant_workflow(self):
        """
        After registrant creation, an event calculate the new registrant state.
        Check if event/workflow works correctly!
        """
        self.form.registrants.invokeFactory('registrant', id='rgs1')
        self.registrant = self.form.registrants['rgs1']
        notify(FormSaveData2ContentEntryFinalizedEvent(self.registrant,
                                                       self.form))
        state = self.pwf.getInfoFor(self.registrant, 'review_state')
        self.assertEqual(state, 'unconfirmed')

        self.form.registrants.invokeFactory('registrant', id='rgs2')
        self.registrant = self.form.registrants['rgs2']
        notify(FormSaveData2ContentEntryFinalizedEvent(self.registrant,
                                                       self.form))
        state = self.pwf.getInfoFor(self.registrant, 'review_state')
        self.assertEqual(state, 'waiting_list_unconfirmed')
