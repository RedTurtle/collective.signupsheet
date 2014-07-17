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
    add_registrant_portal_type(portal)


def setup_signupsheet(portal):
    setup_uwosh_adapter(portal)
    setup_portal_calendar(portal)


def setup_uwosh_adapter(portal):
    types = getToolByName(portal, 'portal_types')
    folder = types[SIGNUPSHEET_TYPE]
    allowed_content_types = set(folder.allowed_content_types)
    allowed_content_types.add('FormSaveData2ContentAdapter')
    folder.allowed_content_types = tuple(allowed_content_types)
    logger.info('D2C adapter added to signup sheet folder')


def setup_portal_calendar(portal):
    #configure portal type
    portal_calendar = getToolByName(portal, 'portal_calendar')
    old_types = portal_calendar.calendar_types
    if SIGNUPSHEET_TYPE in old_types:
        logger.info('SignupSheet is already in calendar_types attribute')
    else:
        new_types = list(old_types) + [SIGNUPSHEET_TYPE, ]
        portal_calendar.calendar_types = tuple(new_types)
        logger.info('SignupSheet added in calendar_types attribute')

    #configure states
    old_states = list(portal_calendar.calendar_states)
    new_states = old_states[:]
    for state in SIGNUPSHEET_STATES:
        if state in old_states:
            msg = u'%s is already in calendar_states attribute' % state
            logger.info(msg)
        else:
            new_states.append(state)
            msg = u"%s will be added to calendar_states attribute" % state
            logger.info(msg)

    if new_states != old_states:
        portal_calendar.calendar_states = tuple(new_states)
        logger.info("portal_calendar.calendare_states updated with new values")


def add_registrant_portal_type(portal):
    name = "registrant"
    portal_types = getToolByName(portal, 'portal_types')
    if name in portal_types.keys():
        logger.error('Registrant is already present in portal_types')
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

    #We need to add registrant also in portal_factory
    factory = getToolByName(portal, 'portal_factory')
    factoryTypes = factory.getFactoryTypes().keys()
    factoryTypes.extend(['registrant'])
    factory.manage_setPortalFactoryTypes(listOfTypeIds=factoryTypes)

    new_type.icon_expr = "string:${portal_url}/registrant.gif"
    logger.info('Add registrant to D2C adapter')
