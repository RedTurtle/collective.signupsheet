# -*- coding: utf-8 -*-

from collective.signupsheet.config import logger


def uninstall(portal, reinstall=False):
    if not reinstall:
        # Don't want to delete all registry values if a Manager simply reinstall the product from ZMI
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-collective.signupsheet:uninstall')

        # remove SignupSheet from linkable object in tiny
        linkable = portal.portal_tinymce.linkable
        if "SignupSheet" in portal.portal_tinymce.linkable:
            portal.portal_tinymce.linkable = linkable.replace('\nSignupSheet', '')
        logger.info("Uninstall done")
