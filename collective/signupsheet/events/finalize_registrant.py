# -*- conding: utf-8 -*-
from zope.component.hooks import getSite
from Products.CMFCore.utils import getToolByName


def finalize_registrant_creation(obj, event):
    """
    we are using a type created from uwosh FormSaveData2ContentEntry.
    So we need to check it by interface and here it's better to perform a check
    on portal_type, 'cause all the type created by uwosh stuff implements
    IFormSaveData2ContentEntry
    """
    if obj.portal_type == 'registrant':
        site = getSite()
        portal_workflow = getToolByName(site, 'portal_workflow')
        portal_membership = getToolByName(site, 'portal_membership')

        if portal_membership.isAnonymousUser():
            obj.setCreators(('(anonymous)',))

        current_state = portal_workflow.getInfoFor(obj, 'review_state')
        if current_state in ('new', ):
            portal_workflow.doActionFor(obj, 'post')
