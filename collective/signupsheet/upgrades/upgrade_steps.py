# -*- coding: utf-8 -*-
from collective.signupsheet.config import logger


def upgrade_0001_to_0002(context):
    """
    This step install some property in the portal_properties tool
    """
    profile = 'profile-collective.signupsheet.upgrades:upgrade_0001_to_0002'
    context.runAllImportStepsFromProfile(profile)
    logger.info("propertiestool.xml imported")
    logger.info("Upgrade from 0001 to 0002 executed")
