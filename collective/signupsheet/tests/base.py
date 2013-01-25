# -*- coding: utf-8 -*-

# Import the base test case classes
from Testing import ZopeTestCase
from Products.CMFPlone.tests import PloneTestCase

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase.layer import onsetup
import Products.PloneFormGen
import uwosh.pfg.d2c
import collective.signupsheet
import os

ZopeTestCase.installProduct('PloneFormGen')


@onsetup
def setup_product():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', Products.PloneFormGen)
    zcml.load_config('configure.zcml', uwosh.pfg.d2c)
    zcml.load_config('configure.zcml', collective.signupsheet)

    ZopeTestCase.installPackage('uwosh.pfg.d2c')
    ZopeTestCase.installPackage('collective.signupsheet')
    fiveconfigure.debug_mode = False


#Set up the Plone site used for the test fixture. The PRODUCTS are the products
#to install in the Plone site (as opposed to the products defined above, which
#are all products available to Zope in the test fixture)
setup_product()
PloneTestCase.setupPloneSite(products=['PloneFormGen',
                                       'uwosh.pfg.d2c',
                                       'collective.signupsheet'])


def get_file(whichone=''):
    if not whichone:
        return None
    path = os.path.join(os.path.dirname(__file__), 'files/' + whichone)
    return file(path, 'r').readlines()


class FunctionalTestCase(PloneTestCase.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
