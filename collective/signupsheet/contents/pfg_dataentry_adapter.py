# NOT USED!!!! WILL'PULL REQUEST A MODIFICATION TO THE ORIGINAL CODE
# REMOVE THIS FILE

"""
The original adapter provided by uwosh.pfg.d2c it's useless with FormFolder
based types 'cause perform some check basing on portal_type 'FormFolder'. So we
create a custom one
"""
from Products.ATContentTypes.content.base import registerATCT

from uwosh.pfg.d2c.contetn.dataentry import FormSaveData2ContentEntry
from zope.interface import implements

from collective.signupsheet.config import PROJECTNAME
from collective.signupsheet.interfaces import ISignupSheetData2ContentEntry


class SignupSheetData2ContentEntry(FormSaveData2ContentEntry):
    implements(ISignupSheetData2ContentEntry)

    meta_type = portal_type = 'SignupSheetData2ContentEntry'
    archetype_name = 'Save Data to Content Entry in Signup Sheet form'

    def getForm(self):
        adapter = self.getFormAdapter()
        if adapter is None:
            adapter = self.getParentNode()

        form = adapter.getParentNode()
        if getattr(form, 'portal_type', None) != 'SignupSheet':
            form = None
        return form

registerATCT(SignupSheetData2ContentEntry, PROJECTNAME)
