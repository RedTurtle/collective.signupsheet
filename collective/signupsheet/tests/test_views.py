# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from collective.signupsheet.tests.base import FunctionalTestCase


class TestBaseView(FunctionalTestCase):
    """
    Test base view configuration used for mainly in ss view
    """

    def afterSetUp(self):
        FunctionalTestCase.afterSetUp(self)
        self.pwf = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Manager', ])
        self.create = self.portal.invokeFactory
        self.newid = self.create(type_name='SignupSheet', id='a-new-form')
        self.form = getattr(self.portal, self.newid)
        self.form.setEventsize(2)
        self.form.setWaitlist_size(2)
        self.form.registrants.invokeFactory(
            'registrant',
            id='rgs1',
            name="john",
            surname="doe",
            email="jdoe@foo.com")

    def test_base_view_status(self):
        view = getMultiAdapter((self.form, self.form.REQUEST),
                                name='susbase_utiltities_view')
        self.assertTrue(view.getSignupStatus() == 'open')
        self.form.registrants.invokeFactory('registrant', id='rgs2')
        self.assertTrue(view.getSignupStatus() == 'open')
        self.form.registrants.invokeFactory('registrant', id='rgs3')
        self.assertTrue(view.getSignupStatus() == 'waitlist')

    def test_base_view_signup_message(self):
        view = getMultiAdapter((self.form, self.form.REQUEST),
                                name='susbase_utiltities_view')
        self.assertTrue(view.getSignupMessage() == 'sign_up')
        self.form.registrants.invokeFactory('registrant', id='rgs2')
        self.assertTrue(view.getSignupMessage() == 'sign_up_for_waitinglist')

    def test_base_view_seatsleft(self):
        view = getMultiAdapter((self.form, self.form.REQUEST),
                                name='susbase_utiltities_view')
        self.assertTrue(view.getSeatsLeft() == 3)
        self.form.registrants.invokeFactory('registrant', id='rgs2')
        self.assertTrue(view.getSeatsLeft() == 2)
        self.form.registrants.invokeFactory('registrant', id='rgs3')
        self.assertTrue(view.getSeatsLeft() == 1)
        self.form.registrants.invokeFactory('registrant', id='rgs4')
        self.assertTrue(view.getSeatsLeft() == 0)

    def test_deadline(self):
        self.assertTrue('Sign up!' in self.form())
        self.form.setRegistrationDeadline(DateTime()-1)
        self.assertFalse('Sign up!' in self.form())

    def test_check_duplicate_registrant(self):
        view = getMultiAdapter((self.form, self.form.REQUEST),
                                name='susbase_utiltities_view')
        duplicate_form = {
            'name': 'john',
            'surname': 'doe',
            'email': "jdoe@foo.com"}
        new_form = {
            'name': 'john',
            'surname': 'baz',
            'email': "jbaz@foo.com"}
        self.assertTrue(view.check_duplicate_registrant(duplicate_form))
        self.assertFalse(view.check_duplicate_registrant(new_form))


class TestDataExport(FunctionalTestCase):
    """
    Test the csv export
    """

    def afterSetUp(self):
        FunctionalTestCase.afterSetUp(self)
        self.pwf = getToolByName(self.portal, 'portal_workflow')
        self.setRoles(['Manager', ])
        self.create = self.portal.invokeFactory
        self.newid = self.create(type_name='SignupSheet', id='a-new-form')
        self.form = getattr(self.portal, self.newid)

        self.form.registrants.invokeFactory('registrant', id='rgs1')
        self.r1 = self.form.registrants['rgs1']
        self.r1.getField('name').set(self.r1, 'John')
        self.r1.getField('surname').set(self.r1, 'Dillinger')
        self.r1.getField('email').set(self.r1, 'john.dillinger@mailprovider.com')

        self.form.registrants.invokeFactory('registrant', id='rgs2')
        self.r2 = self.form.registrants['rgs2']
        self.r2.getField('name').set(self.r2, 'Frank')
        self.r2.getField('surname').set(self.r2, 'Lukas')
        self.r2.getField('email').set(self.r2, 'frank.lukas@mailprovider.com')

    def test_csv_export(self):
        view = getMultiAdapter((self.form, self.form.REQUEST),
                               name="registrants_data_export")
        #test_csv = get_file('csv_test.csv')
        csv = view.generateCSV(fields=['name', 'surname'],
                               delimiter='colon')
        #We have something
        self.assertTrue(csv != '')

        lines = csv.split('\r\n')
        #Check header
        self.assertTrue(lines[0].split(':') == ['date', 'id', 'name', 'surname',
                                                'review_state'])

        #Check if we have export all registrants
        #filter: exclude empty last values coming from split
        self.assertTrue(len(filter(bool, lines)) == 3)
        csv = view.generateCSV(fields=['name', 'surname', 'email'],
                               delimiter='semicolon')

        #Check with a more real export
        lines = csv.split('\r\n')
        self.assertTrue(lines[0].split(';') == ['date', 'id',
                                                'name', 'surname', 'email',
                                                'review_state'])
        self.assertTrue(lines[1].split(';')[1] == 'rgs1')
        self.assertTrue(lines[1].split(';')[2] == 'John')
        self.assertTrue(lines[1].split(';')[3] == 'Dillinger')
        self.assertTrue(lines[1].split(';')[4] == 'john.dillinger@mailprovider.com')
