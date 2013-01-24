# -*- coding: utf-8 -*-

from AccessControl import ModuleSecurityInfo
from Products.Archetypes import atapi
from Products.CMFCore import utils

from zope.i18nmessageid import MessageFactory
signupsheetMessageFactory = MessageFactory('collective.signupsheet')
ModuleSecurityInfo('collective.signupsheet').declarePublic('signupsheetMessageFactory')

from collective.signupsheet import config


def initialize(context):
    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype, ),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,),
            ).initialize(context)
