# -*- conding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.component import getUtility

from collective.signupsheet.interfaces import IGetRegistrants


def compute_next_action(obj, signupsheet):
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
        action = 'post'
    else:
        action = 'post_waitinglist'
    return action


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
            signupsheet = obj.getForm()
            action = compute_next_action(obj, signupsheet)
            portal_workflow.doActionFor(obj, action)

        if portal_membership.isAnonymousUser():
            obj.setCreators(('(anonymous)',))
