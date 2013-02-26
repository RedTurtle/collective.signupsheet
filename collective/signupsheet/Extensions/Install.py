# -*- coding: utf-8 -*-

from collective.signupsheet.config import logger
SIGNUPSHEETTYPE = "SignupSheet"


def uninstall(portal, reinstall=False):
    if not reinstall:
        # Don't want to delete all registry values if a Manager simply reinstall the product from ZMI
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-collective.signupsheet:uninstall')

        # remove SignupSheet from linkable object in tiny
        linkable = portal.portal_tinymce.linkable
        if SIGNUPSHEETTYPE in portal.portal_tinymce.linkable:
            portal.portal_tinymce.linkable = linkable.replace('\nSignupSheet', '')
            logger.info("Remove SignupSheet from linkable type in TinyMCE")

        if SIGNUPSHEETTYPE in portal.portal_calendar.calendar_types:
            types = list(portal.portal_calendar.calendar_types)
            types.remove(SIGNUPSHEETTYPE)
            portal.portal_calendar.calendar_types = tuple(types)
            logger.info("Remove SignupSheet from portal_calendar.calendar_types")

        logger.info("Uninstall done")
