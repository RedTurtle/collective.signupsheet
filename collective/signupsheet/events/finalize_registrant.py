# -*- conding: utf-8 -*-

from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.component import getUtility

from collective.signupsheet.interfaces import IGetRegistrants


def compute_and_set_status(obj, signupsheet):
    """
    if we don't get any value from the form we decide to compute the value in
    this way.
    """
    utility = getUtility(IGetRegistrants)
    registrant_folder = utility.get_registrants_folder(signupsheet)
    event_size = signupsheet.getEventsize()
    current_size = len(
                    registrant_folder.contentIds(
                            filter={'portal_type': 'registrant'}
                       )
                    )
    if current_size <= event_size or event_size == 0:
        status = 'registered'
    else:
        status = 'waitinglist'

    setattr(obj, 'ssfg_status', status)


def finalize_registrant_creation(obj, event):
    """
    we are using a type created from uwosh FormSaveData2ContentEntry.
    So we need to get it by interface to cath the event, but here we need to
    check on portal_type, 'cause all the type created by uwosh stuff implements
    IFormSaveData2ContentEntry
    """
    # change the object state
    if obj.portal_type == 'registrant':
        site = getSite()
        portal_workflow = getToolByName(site, 'portal_workflow')
        portal_membership = getToolByName(site, 'portal_membership')

        current_state = portal_workflow.getInfoFor(obj, 'review_state')
        if current_state in ('new', ):
            portal_workflow.doActionFor(obj, 'post')

        if portal_membership.isAnonymousUser():
            obj.setCreators(('(anonymous)',))

        # set the status for the object if needed:
        # if we have anonymous/not-manager registration we need to set the value
        # if we have a manager-registration we could have or not the value,
        # 'cause it's not mandatory in the form
        signupsheet = obj.getForm()
        form_fields_list = [field.__name__ for field in signupsheet.values()]
        if 'ssfg_status' in form_fields_list:
            have_status = shasattr(obj, 'ssfg_status')
            if not have_status:
                compute_and_set_status(obj, signupsheet)
            elif have_status and not obj.getField('ssfg_status').get(obj):
                compute_and_set_status(obj, signupsheet)
            else:
                pass
