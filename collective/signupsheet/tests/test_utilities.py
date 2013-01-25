# -*- coding: utf-8 -*-
from zope.component import getUtility

from collective.signupsheet.interfaces import IGetRegistrants
from collective.signupsheet.tests.base import FunctionalTestCase


class TestUtilities(FunctionalTestCase):
    """
    Use this test class to test SignupSheet utilities
    """

    def afterSetUp(self):
        FunctionalTestCase.afterSetUp(self)
        self.setRoles(['Manager', ])
        self.create = self.portal.invokeFactory
        self.newid = self.create(type_name='SignupSheet', id='a-new-form')
        self.form = getattr(self.portal, self.newid)
        self.form.registrants.invokeFactory('registrant', id='rgs1')
        self.form.registrants.invokeFactory('registrant', id='rgs2')
        self.form.registrants.invokeFactory('registrant', id='rgs3')

    def test_utitlities(self):
        utility = getUtility(IGetRegistrants)
        self.assertEqual(3, len(utility.get_registrants_brains(self.form)))
        regfolder = utility.get_registrants_folder(self.form).absolute_url()
        self.assertEqual('http://nohost/plone/a-new-form/registrants',
                            regfolder)
        regs = utility.get_registrants(self.form)
        self.assertEqual(3, len(regs))
        self.assertEqual('FormSaveData2ContentEntry',
                            regs[0].__class__.__name__)
