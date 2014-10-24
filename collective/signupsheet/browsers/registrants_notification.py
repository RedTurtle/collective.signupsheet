# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from collective.signupsheet.interfaces import IGetRegistrants
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility


class RegistrantNotificationView(BrowserView):
    """View for sending email to registrants"""
    
    def __call__(self, *args, **kwargs):
        return self.index()
    
    def registrants(self):
        utility = getUtility(IGetRegistrants)
        wtool = getToolByName(self.context, 'portal_workflow')
        registrants = utility.get_registrants(self.context)
        results = []
        for registrant in registrants:
            data = dict(id=registrant.id,
                        name=registrant.title_or_id(),
                        email=registrant.email,
                        review_state=wtool.getInfoFor(registrant, 'review_state'))
            results.append(data)
        return results
