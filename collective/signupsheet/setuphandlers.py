# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility

from collective.signupsheet import signupsheetMessageFactory as _
import logging
import zope.i18n


def setupVarious(context):
    if context.readDataFile('collective.signupsheet_various.txt') is None:
        return
    portal = context.getSite()
    addNewTypeToSignupSheet(portal)
    setupNewPortalTypes(portal)


def addNewTypeToSignupSheet(portal):
    types = getToolByName(portal, 'portal_types')
    if 'SignupSheet' in types.objectIds():
        folder = types['SignupSheet']
        allowed_content_types = set(folder.allowed_content_types)
        allowed_content_types.add('FormSaveData2ContentAdapter')
        folder.allowed_content_types = tuple(allowed_content_types)
        msg = zope.i18n.translate(
                        _(u'add_d2c_adapter_to_signupsheet',
                          u'D2C adapter add to signup sheet folder'),
                          context=portal.REQUEST)
        logging.info(msg)
        return
    msg = zope.i18n.translate(
                        _(u'add_d2c_adapter_to_signupsheet_error',
                          u'Error adding D2C adapter to signup sheet folder'),
                          context=portal.REQUEST)
    logging.error(msg)


def setupNewPortalTypes(portal):
    """
    Use the same method used in uwosh.pfg.d2c to create the new content type
    we'll use as event subscriber.
    """
    name = "registrant"
    portal_types = getToolByName(portal, 'portal_types')
    if name in portal_types.keys():
        msg = zope.i18n.translate(
                        _(u'error_message_install_registrant',
                          u'Registrant it\'s already present in portal_types'),
                          context=portal.REQUEST)
        logging.error(msg)
        return
    data = portal_types.manage_copyObjects(['FormSaveData2ContentEntry'])
    res = portal_types.manage_pasteObjects(data)
    id = res[0]['new_id']
    normalizer = getUtility(IIDNormalizer)
    new_id = normalizer.normalize(name)
    # BBB think we can remove this...
    count = 1
    while new_id in portal_types.objectIds():
        new_id = normalizer.normalize(name + str(count))
        count += 1

    portal_types.manage_renameObject(id, new_id)
    new_type = portal_types[new_id]
    new_type.title = name
    new_type.icon_expr = "string:${portal_url}/registrant.gif"
    msg = zope.i18n.translate(
                        _(u'create_new_d2c_type',
                          u'Add registrant to D2C adapter'),
                          context=portal.REQUEST)
    logging.info(msg)
    return
