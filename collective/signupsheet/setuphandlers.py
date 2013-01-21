# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility

from collective.signupsheet.config import logger

SIGNUPSHEET_TYPE = 'SignupSheet'
SIGNUPSHEET_STATES = ['open', 'closed', ]


def setupVarious(context):
    if context.readDataFile('collective.signupsheet_various.txt') is None:
        return
    portal = context.getSite()
    setup_signupsheet(portal)
    setup_registrant_portal_type(portal)


def setup_signupsheet(portal):
    setup_uwosh_adapter(portal)
    setup_portal_calendar(portal)


def setup_uwosh_adapter(portal):
    types = getToolByName(portal, 'portal_types')
    if SIGNUPSHEET_TYPE in types.objectIds():
        folder = types[SIGNUPSHEET_TYPE]
        allowed_content_types = set(folder.allowed_content_types)
        allowed_content_types.add('FormSaveData2ContentAdapter')
        folder.allowed_content_types = tuple(allowed_content_types)
        msg = u'D2C adapter add to signup sheet folder'
        logger.info(msg)
        return
    msg = u'Error adding D2C adapter to signup sheet folder'
    logger.error(msg)


def setup_portal_calendar(portal):
    #configure portal type
    portal_calendar = getToolByName(portal, 'portal_calendar')
    old_types = portal_calendar.calendar_types
    if SIGNUPSHEET_TYPE in old_types:
        msg = u'SignupSheet it\'s already in calendar_types attribute'
        logger.info(msg)
    else:
        new_types = list(old_types) + [SIGNUPSHEET_TYPE, ]
        portal_calendar.calendar_types = tuple(new_types)
        msg = u'SignupSheet added in calendar_types attribute'
        logger.info(msg)

    #configure states
    old_states = list(portal_calendar.calendar_states)
    new_states = old_states[:]
    for state in SIGNUPSHEET_STATES:
        if state in old_states:
            msg = u'%s it\'s already in calendar_states attribute' % state
            logger.info(msg)
        else:
            new_states.append(state)
            msg = u"%s will be added to calendar_states attribute" % state
            logger.info(msg)

    if new_states != old_states:
        portal_calendar.calendar_states = tuple(new_states)
        msg = u"portal_calendar.calendare_states updatet with new values"
        logger.info(msg)


def setup_registrant_portal_type(portal):
    """
    Use the same method used in uwosh.pfg.d2c to create the new content type
    we'll use as event subscriber.
    """
    add_registrant_portal_type(portal)


def add_registrant_portal_type(portal):
    name = "registrant"
    portal_types = getToolByName(portal, 'portal_types')
    if name in portal_types.keys():
        msg = u'Registrant it\'s already present in portal_types'
        logger.error(msg)
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
    msg = u'Add registrant to D2C adapter'
    logger.info(msg)
    return
